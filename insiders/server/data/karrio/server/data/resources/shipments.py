import json
from django.db.models import Q
from import_export import resources

from karrio.core.utils import DP, DF
from karrio.core.units import Packages
from karrio.server.core import serializers
from karrio.server.core import datatypes as types, dataunits as units
from karrio.server.manager import models
from karrio.server.core.filters import ShipmentFilters

DEFAULT_HEADERS = {
    "id": "ID",
    "created_at": "Created at",
    "tracking_number": "Tracking number",
    "status": "Status",
    "shipper_id": "Shipper ID",
    "shipper_name": "Shipper name",
    "shipper_company": "Shipper Company",
    "shipper_address_line1": "Shipper address line 1",
    "shipper_address_line2": "Shipper address line 2",
    "shipper_city": "Shipper city",
    "shipper_state": "Shipper state",
    "shipper_postal_code": "Shipper postal code",
    "shipper_country": "Shipper country",
    "shipper_residential": "Shipper residential",
    "recipient_id": "Recipient ID",
    "recipient_name": "Recipient name",
    "recipient_company": "Recipient Company",
    "recipient_address_line1": "Recipient address line 1",
    "recipient_address_line2": "Recipient address line 2",
    "recipient_city": "Recipient city",
    "recipient_state": "Recipient state",
    "recipient_postal_code": "Recipient postal code",
    "recipient_country": "Recipient country",
    "recipient_residential": "Recipient residential",
    "weight": "Weight",
    "weight_unit": "Weight unit",
    "pieces": "Number of pieces",
    "service": "Service",
    "carrier": "Carrier",
    "rate": "Rate",
    "currency": "Currency",
    "paid_by": "Payor",
    "reference": "Reference",
    "options": "Options",
}


def shipment_resource(query_params: dict, context, **kwargs):
    queryset = models.Shipment.access_by(context)
    _exclude = query_params.get("exclude", "").split(",")
    _fields = (
        "id",
        "tracking_number",
        "created_at",
        "status",
        "reference",
    )

    if "status" not in query_params:
        queryset = queryset.filter(
            Q(status__in=["purchased", "delivered", "shipped", "in_transit"]),
        )

    class Resource(resources.ModelResource):
        class Meta:
            model = models.Shipment
            fields = _fields
            exclude = _exclude
            export_order = [k for k in DEFAULT_HEADERS.keys() if k not in _exclude]

        def get_queryset(self):
            return ShipmentFilters(query_params, queryset).qs

        def get_export_headers(self):
            headers = super().get_export_headers()
            return [DEFAULT_HEADERS.get(k, k) for k in headers]

        if "service" not in _exclude:
            service = resources.Field()

            def dehydrate_service(self, row):
                rate = getattr(row, "selected_rate") or {}
                return (rate.get("meta") or {}).get("service_name") or rate.get(
                    "service"
                )

        if "carrier" not in _exclude:
            carrier = resources.Field()

            def dehydrate_carrier(self, row):
                carrier = getattr(row, "selected_rate_carrier", None)
                settings = getattr(carrier, "settings", None)
                return getattr(
                    settings,
                    "display_name",
                    units.REFERENCE_MODELS["carriers"][carrier.carrier_name],
                )

        if "pieces" not in _exclude:
            pieces = resources.Field()

            def dehydrate_pieces(self, row):
                return len(row.parcels.all())

        if "rate" not in _exclude:
            rate = resources.Field()

            def dehydrate_rate(self, row):
                return (getattr(row, "selected_rate") or {}).get("total_charge", None)

        if "currency" not in _exclude:
            currency = resources.Field()

            def dehydrate_currency(self, row):
                return (getattr(row, "selected_rate") or {}).get("currency", None)

        if "paid_by" not in _exclude:
            paid_by = resources.Field()

            def dehydrate_paid_by(self, row):
                return (getattr(row, "payment") or {}).get("paid_by", None)

        if "weight" not in _exclude:
            weight = resources.Field()
            weight_unit = resources.Field()

            @staticmethod
            def packages(row):
                parcels = serializers.Parcel(row.parcels, many=True).data
                return Packages([DP.to_object(types.Parcel, p) for p in parcels])

            def dehydrate_weight(self, row):
                return self.packages(row).weight.value

            def dehydrate_weight_unit(self, row):
                return self.packages(row).weight.unit

        if "shipment_date" not in _exclude:
            shipment_date = resources.Field()

            def dehydrate_shipment_date(self, row):
                return (getattr(row, "options") or {}).get("shipment_date", None) or (
                    DF.fdate(row.created_at, "%Y-%m-%m %H:%M:%M")
                )

        if "shipper_id" not in _exclude:
            shipper_id = resources.Field()

            def dehydrate_shipper_id(self, row):
                return row.shipper.id

        if "shipper_name" not in _exclude:
            shipper_name = resources.Field()

            def dehydrate_shipper_name(self, row):
                return row.shipper.person_name

        if "shipper_company" not in _exclude:
            shipper_company = resources.Field()

            def dehydrate_shipper_company(self, row):
                return row.shipper.company_name

        if "shipper_address_line1" not in _exclude:
            shipper_address_line1 = resources.Field()

            def dehydrate_shipper_address_line1(self, row):
                return row.shipper.address_line1

        if "shipper_address_line2" not in _exclude:
            shipper_address_line2 = resources.Field()

            def dehydrate_shipper_address_line2(self, row):
                return row.shipper.address_line2

        if "shipper_city" not in _exclude:
            shipper_city = resources.Field()

            def dehydrate_shipper_city(self, row):
                return row.shipper.city

        if "shipper_state" not in _exclude:
            shipper_state = resources.Field()

            def dehydrate_shipper_state(self, row):
                return row.shipper.state_code

        if "shipper_postal_code" not in _exclude:
            shipper_postal_code = resources.Field()

            def dehydrate_shipper_postal_code(self, row):
                return row.shipper.postal_code

        if "shipper_country" not in _exclude:
            shipper_country = resources.Field()

            def dehydrate_shipper_country(self, row):
                return row.shipper.country_code

        if "shipper_residential" not in _exclude:
            shipper_residential = resources.Field()

            def dehydrate_shipper_residential(self, row):
                return row.shipper.residential

        if "recipient_id" not in _exclude:
            recipient_id = resources.Field()

            def dehydrate_recipient_id(self, row):
                return row.recipient.id

        if "recipient_name" not in _exclude:
            recipient_name = resources.Field()

            def dehydrate_recipient_name(self, row):
                return row.recipient.person_name

        if "recipient_company" not in _exclude:
            recipient_company = resources.Field()

            def dehydrate_recipient_company(self, row):
                return row.recipient.company_name

        if "recipient_address_line1" not in _exclude:
            recipient_address_line1 = resources.Field()

            def dehydrate_recipient_address_line1(self, row):
                return row.recipient.address_line1

        if "recipient_address_line2" not in _exclude:
            recipient_address_line2 = resources.Field()

            def dehydrate_recipient_address_line2(self, row):
                return row.recipient.address_line2

        if "recipient_city" not in _exclude:
            recipient_city = resources.Field()

            def dehydrate_recipient_city(self, row):
                return row.recipient.city

        if "recipient_state" not in _exclude:
            recipient_state = resources.Field()

            def dehydrate_recipient_state(self, row):
                return row.recipient.state_code

        if "recipient_postal_code" not in _exclude:
            recipient_postal_code = resources.Field()

            def dehydrate_recipient_postal_code(self, row):
                return row.recipient.postal_code

        if "recipient_country" not in _exclude:
            recipient_country = resources.Field()

            def dehydrate_recipient_country(self, row):
                return row.recipient.country_code

        if "recipient_residential" not in _exclude:
            recipient_residential = resources.Field()

            def dehydrate_recipient_residential(self, row):
                return row.recipient.residential

        if "options" not in _exclude:
            options = resources.Field()

            def dehydrate_options(self, row):
                return json.loads(json.dumps(row.options))

    return Resource()
