# Generated by Django 4.1.3 on 2022-11-28 18:52

from django.db import migrations
import functools
import karrio.lib as lib
import karrio.references as ref
import karrio.server.core.fields
import karrio.server.core.models


def forwards_func(apps, schema_editor):
    import karrio.server.providers.models as providers

    db_alias = schema_editor.connection.alias
    Carrier = apps.get_model("providers", "Carrier")
    _carriers = []

    for carrier in Carrier.objects.using(db_alias).all():
        carrier_name, _ = providers.Carrier.resolve_settings(carrier)
        raw_capabilities = ref.get_carrier_capabilities(carrier_name)
        carrier.carrier_capabilities = [
            c for c in lib.to_dict(carrier.capabilities) if c in raw_capabilities
        ]
        _carriers.append(carrier)

    Carrier.objects.using(db_alias).bulk_update(_carriers, ["carrier_capabilities"])


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("providers", "0043_alter_genericsettings_account_number_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="carrier",
            name="carrier_capabilities",
            field=karrio.server.core.fields.MultiChoiceField(
                choices=[
                    ("pickup", "pickup"),
                    ("rating", "rating"),
                    ("shipping", "shipping"),
                    ("tracking", "tracking"),
                    ("paperless", "paperless"),
                ],
                default=functools.partial(
                    karrio.server.core.models._identity, *(), **{"value": []}
                ),
                help_text="Select the capabilities of the carrier that you want to enable",
            ),
        ),
        migrations.RunPython(forwards_func, reverse_func),
        migrations.RemoveField(model_name="carrier", name="capabilities"),
        migrations.RenameField(
            model_name="carrier",
            old_name="carrier_capabilities",
            new_name="capabilities",
        ),
    ]
