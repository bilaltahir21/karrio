# Generated by Django 3.2.14 on 2022-08-28 01:41

from django.db import migrations, models
import karrio.server.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pricing', '0024_auto_20220808_0803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surcharge',
            name='carriers',
            field=karrio.server.core.fields.MultiChoiceField(base_field=models.CharField(choices=[('amazon_mws', 'amazon_mws'), ('aramex', 'aramex'), ('australiapost', 'australiapost'), ('canadapost', 'canadapost'), ('canpar', 'canpar'), ('dhl_express', 'dhl_express'), ('dhl_poland', 'dhl_poland'), ('dhl_universal', 'dhl_universal'), ('dicom', 'dicom'), ('dpdhl', 'dpdhl'), ('easypost', 'easypost'), ('eshipper', 'eshipper'), ('fedex', 'fedex'), ('freightcom', 'freightcom'), ('generic', 'generic'), ('purolator', 'purolator'), ('royalmail', 'royalmail'), ('sendle', 'sendle'), ('sf_express', 'sf_express'), ('tnt', 'tnt'), ('ups', 'ups'), ('ups_freight', 'ups_freight'), ('usps', 'usps'), ('usps_international', 'usps_international'), ('yanwen', 'yanwen'), ('yunexpress', 'yunexpress')], max_length=50), blank=True, help_text='\n        The list of carriers you want to apply the surcharge to.\n        <br/>\n        Note that by default, the surcharge is applied to all carriers\n        ', null=True, size=None),
        ),
    ]
