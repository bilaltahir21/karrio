# Generated by Django 3.2.14 on 2022-09-03 12:56

from django.db import migrations, models
import functools
import karrio.server.core.fields
import karrio.server.core.models
import karrio.server.core.models.base


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0008_auto_20220817_0107'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizationuser',
            name='roles',
            field=karrio.server.core.fields.MultiChoiceField(base_field=models.CharField(choices=[('member', 'member'), ('developer', 'developer'), ('admin', 'admin')], max_length=50), default=functools.partial(karrio.server.core.models._identity, *(), **{'value': ['member', 'developer']}), size=None),
        ),
        migrations.AlterField(
            model_name='organizationuser',
            name='id',
            field=models.CharField(default=functools.partial(karrio.server.core.models.base.uuid, *(), **{'prefix': 'usr_'}), editable=False, max_length=50, primary_key=True, serialize=False),
        ),
    ]
