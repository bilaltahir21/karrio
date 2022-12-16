import functools
import operator
import typing
import logging
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes import models as contenttypes
from rest_framework import exceptions

import karrio.server.core.utils as utils
import karrio.server.user.models as users
import karrio.server.orgs.models as orgs
import karrio.server.iam.serializers as serializers
import karrio.server.iam.models as iam

logger = logging.getLogger(__name__)
User = get_user_model()


@utils.skip_on_loadata
@utils.async_wrapper
@utils.tenant_aware
def setup_groups(**_):
    """This function create all standard group permissions if they don't exsist."""

    # manage_apps
    setup_group(
        serializers.PermissionGroup.manage_apps.name,
        permissions=Permission.objects.filter(content_type__app_label="apps"),
    )

	# manage_carriers
    setup_group(
        serializers.PermissionGroup.manage_carriers.name,
        permissions=[
            *Permission.objects.filter(content_type__app_label="providers"),
            *Permission.objects.filter(
                models.Q(content_type__app_label="orgs") & models.Q(name__contains="carrier")
            )
        ],
        override=True,
    )

	# manage_orders
    setup_group(
        serializers.PermissionGroup.manage_orders.name,
        permissions=Permission.objects.filter(content_type__app_label="orders"),
    )

	# manage_team
    setup_group(
        serializers.PermissionGroup.manage_team.name,
        permissions=(
            Permission.objects
            .filter(content_type__app_label="orgs", name__contains="organization")
            .exclude(name__contains="owner")
        ),
        override=True
    )

	# manage_org_owner
    setup_group(
        serializers.PermissionGroup.manage_org_owner.name,
        permissions=Permission.objects.filter(content_type__model="OrganizationOwner".lower()),
    )

	# manage_webhooks
    setup_group(
        serializers.PermissionGroup.manage_webhooks.name,
        permissions=Permission.objects.filter(content_type__model="Webhook".lower()),
    )

	# manage_data
    setup_group(
        serializers.PermissionGroup.manage_data.name,
        permissions=[
            *Permission.objects.filter(content_type__app_label__in=[
                "data", "graph", "documents"
            ]),
            *Permission.objects.filter(content_type__app_label="audit", name__contains="view"),
            *Permission.objects.filter(content_type__app_label="rest_framework_tracking", name__contains="view")
        ],
        override=True,
    )

	# manage_shipments
    setup_group(
        serializers.PermissionGroup.manage_shipments.name,
        permissions=[
            *Permission.objects.filter(content_type__app_label="manager"),
            *Permission.objects.filter(
                models.Q(content_type__app_label="orgs") & (
                    models.Q(name__contains="address") |
                    models.Q(name__contains="parcel") |
                    models.Q(name__contains="commodity") |
                    models.Q(name__contains="customs") |
                    models.Q(name__contains="pickup") |
                    models.Q(name__contains="tracker") |
                    models.Q(name__contains="shipment")
                ))
        ],
    )

	# manage_system
    setup_group(
        serializers.PermissionGroup.manage_system.name,
        permissions=Permission.objects.filter(content_type__app_label__in=[
            "admin", "user", "pricing", "providers", "audit",
            "database", "rest_framework_tracking",
        ]),
    )


@utils.skip_on_loadata
@utils.async_wrapper
@utils.tenant_aware
def apply_for_org_users(**_):
    """This function will create context permissions for all organization users based on their roles."""
    org_user_permissions = (
        iam.ContextPermission.objects
        .filter(content_type__model="OrganizationUser".lower())
        .values_list('id')
    )
    org_users_without_permissions = orgs.OrganizationUser.objects.all().exclude(
        id__in=list(org_user_permissions)
    )

    for user in org_users_without_permissions:
        sync_permissions(user)


def setup_group(name: str, permissions: typing.List[Permission], override: bool = False):
    group, created = users.Group.objects.get_or_create(name=name)

    if created or override:
        group.permissions.set(permissions)
        group.save()


def sync_permissions(org_user):
    org_owner_id = utils.failsafe(lambda: org_user.organization.owner.organization_user.id)
    group_names = set(
        sum(
            [
                serializers.ROLES_GROUPS.get(role) or []
                for role in org_user.roles
            ],
            start=[],
        )
    )

    if org_owner_id == org_user.id:
        group_names.add("manage_org_owner")

    groups = users.Group.objects.filter(name__in=group_names)

    permission, _ = iam.ContextPermission.objects.get_or_create(
        content_type=contenttypes.ContentType.objects.get_for_model(org_user),
        object_pk=org_user.pk,
    )
    permission.groups.set(groups)
    permission.save()


def check_context_permissions(context=None, keys: typing.List[str] = [], **kwargs):
    groups = [group for group, _ in serializers.PERMISSION_GROUPS if group in keys]

    if any(groups) and users.Group.objects.exists():
        user = (
            context.org.organization_users.filter(user__id=context.user.id)
            if settings.MULTI_ORGANIZATIONS
            else User.objects.filter(id=context.user.id)
        ).first()
        token = getattr(context, "token", None)
        group_filters = functools.reduce(
            operator.and_, (models.Q(groups__name=x) for x in groups)
        )
        token_permission = iam.ContextPermission.objects.filter(
            models.Q(object_pk=getattr(token, "pk", None))
        )

        if token_permission.exists():
            permission_groups = token_permission.filter(group_filters)
        else:
            permission_groups = iam.ContextPermission.objects.filter(
                models.Q(object_pk=user.pk) & group_filters
            )

        if not permission_groups.exists():
            raise exceptions.PermissionDenied()

