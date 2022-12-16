import typing
import logging
import functools
import strawberry
from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from django.utils.translation import gettext_lazy as _
from django_email_verification.confirm import (
    _get_validated_field,
    EmailMultiAlternatives,
    render_to_string,
)

import karrio.lib as lib
import karrio.server.conf as conf
import karrio.server.core.utils as utils
import karrio.server.orgs.models as models
import karrio.server.orgs.serializers as serializers

User = get_user_model()
logger = logging.getLogger(__name__)
OrganizationUserRole: typing.Any = strawberry.enum(serializers.UserRole)


def roles_required(roles: typing.List[OrganizationUserRole]):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(info, **kwargs):
            user = info.context.request.user
            org_id = kwargs.get("id") or kwargs.get("org_id")
            org = (
                models.Organization.objects.filter(id=org_id, is_active=True).first()
                if org_id
                else getattr(info.context.request, "org", None)
            )
            org_user = org.organization_users.filter(user=user).first() if org else None

            if user.is_anonymous:
                raise exceptions.NotAuthenticated()

            if org is None:
                raise exceptions.NotFound("No active organization found")

            if not all(
                [
                    OrganizationUserRole[role] in getattr(org_user, "roles", [])
                    for role in roles
                ]
            ):
                raise exceptions.PermissionDenied()

            kwargs.update({"org": org})

            return func(info, **kwargs)

        return wrapper

    return decorator


def admin_required(instance, context) -> models.Organization:
    organization = (
        instance.organization if hasattr(instance, "organization") else instance
    )
    if not organization.organization_users.filter(
        is_admin=True, user__id=context.request.user.id
    ).exists():
        raise exceptions.PermissionDenied()

    return instance


@utils.email_setup_required
def send_invitation_emails(
    organization: models.Organization,
    emails: typing.List[str],
    redirect_url: str,
    invited_by: User,  # type:ignore
):
    @transaction.atomic
    def action(email: str):
        invitation = models.OrganizationInvitation.objects.create(
            invitee_identifier=email,
            invited_by=invited_by,
            invitee=User.objects.filter(email=email).first(),
            organization_id=organization.id,
        )
        send_invitation(invitation, organization, redirect_url)
        organization.organization_invites.add(invitation)

    exclusion = [
        *organization.users.all().values_list("email", flat=True),
        *organization.organization_invites.all().values_list(
            "invitee_identifier", flat=True
        ),
    ]
    return lib.run_concurently(action, [email for email in emails if email not in exclusion])


def send_invitation(
    invitation: models.OrganizationInvitation,
    organization: models.Organization,
    redirect_url: str,
):
    owner = getattr(organization, "owner", None)
    sender = _get_validated_field("EMAIL_FROM_ADDRESS")
    invited_by = invitation.invited_by.full_name or "You are"
    redirect_link = f"{redirect_url}?token={invitation.guid}"
    subject = f"{invited_by} invited you to join the {organization.name} team on {conf.settings.APP_NAME}"
    context = {
        "redirect_link": redirect_link,
        "app_name": conf.settings.APP_NAME,
        "organization_name": organization.name,
        "owner_email": getattr(owner, "email", invitation.invited_by.email),
    }

    text = render_to_string("karrio/invitation_email.html", context)
    html = render_to_string("karrio/invitation_email.html", context)

    logger.info(f"Sending invitation email to {invitation.invitee_identifier}")

    msg = EmailMultiAlternatives(subject, text, sender, [invitation.invitee_identifier])
    msg.attach_alternative(html, "text/html")
    msg.send()
