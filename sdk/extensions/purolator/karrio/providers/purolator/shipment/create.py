from purolator_lib.shipping_documents_service_1_3_0 import DocumentDetail
from purolator_lib.shipping_service_2_1_3 import (
    CreateShipmentRequest,
    PIN,
    Shipment,
    SenderInformation,
    ReceiverInformation,
    PackageInformation,
    TrackingReferenceInformation,
    Address,
    InternationalInformation,
    PickupInformation,
    PickupType,
    ArrayOfPiece,
    Piece,
    Weight as PurolatorWeight,
    WeightUnit as PurolatorWeightUnit,
    RequestContext,
    Dimension as PurolatorDimension,
    DimensionUnit as PurolatorDimensionUnit,
    TotalWeight,
    PhoneNumber,
    PaymentInformation,
    DutyInformation,
    NotificationInformation,
    ArrayOfOptionIDValuePair,
    OptionIDValuePair,
    BusinessRelationship,
    PrinterType,
    ContentDetail,
    ArrayOfContentDetail,
)

import typing
import functools
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.purolator.error as provider_error
import karrio.providers.purolator.units as provider_units
import karrio.providers.purolator.utils as provider_utils
import karrio.providers.purolator.shipment.documents as documents


def parse_shipment_response(
    response: lib.Element, settings: provider_utils.Settings
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    pin = lib.find_element("ShipmentPIN", response, PIN, first=True)
    shipment = (
        _extract_shipment(response, settings)
        if (getattr(pin, "Value", None) is not None)
        else None
    )

    return shipment, provider_error.parse_error_response(response, settings)


def _extract_shipment(
    response: lib.Element,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    pin: PIN = lib.find_element("ShipmentPIN", response, PIN, first=True)
    documents = lib.find_element("DocumentDetail", response, DocumentDetail)
    label = next((doc for doc in documents if "BillOfLading" in doc.DocumentType), DocumentDetail())
    invoice = next((doc for doc in documents if "Invoice" in doc.DocumentType), None)

    return models.ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=pin.Value,
        shipment_identifier=pin.Value,
        docs=models.Documents(
            label=getattr(label, "Data", ""),
            **(dict(invoice=invoice.Data) if invoice else {}),
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable[lib.Pipeline]:
    requests: lib.Pipeline = lib.Pipeline(
        create=lambda *_: functools.partial(
            _create_shipment, payload=payload, settings=settings
        )(),
        document=functools.partial(
            _get_shipment_label, payload=payload, settings=settings
        ),
    )
    return lib.Serializable(requests)


def _shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable[lib.Envelope]:
    packages = lib.to_packages(
        payload.parcels,
        provider_units.PackagePresets,
        required=["weight"],
    )
    service = provider_units.ShippingService.map(payload.service).value_or_key
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    is_international = payload.shipper.country_code != payload.recipient.country_code
    shipper_phone_number = units.Phone(
        payload.shipper.phone_number or "000 000 0000", payload.shipper.country_code
    )
    recipient_phone_number = units.Phone(
        payload.recipient.phone_number or "000 000 0000", payload.recipient.country_code
    )
    printing = provider_units.PrintType.map(payload.label_type or "PDF").value

    request = lib.create_envelope(
        header_content=RequestContext(
            Version="2.1",
            Language=settings.language,
            GroupID="",
            RequestReference=(getattr(payload, "id", None) or ""),
            UserToken=settings.user_token,
        ),
        body_content=CreateShipmentRequest(
            Shipment=Shipment(
                SenderInformation=SenderInformation(
                    Address=Address(
                        Name=payload.shipper.person_name,
                        Company=payload.shipper.company_name,
                        Department=None,
                        StreetNumber="",
                        StreetSuffix=None,
                        StreetName=lib.join(payload.shipper.address_line1, join=True),
                        StreetType=None,
                        StreetDirection=None,
                        Suite=None,
                        Floor=None,
                        StreetAddress2=lib.join(
                            payload.shipper.address_line2, join=True
                        ),
                        StreetAddress3=None,
                        City=payload.shipper.city or "",
                        Province=payload.shipper.state_code or "",
                        Country=payload.shipper.country_code or "",
                        PostalCode=payload.shipper.postal_code or "",
                        PhoneNumber=PhoneNumber(
                            CountryCode=shipper_phone_number.country_code or "0",
                            AreaCode=shipper_phone_number.area_code or "0",
                            Phone=shipper_phone_number.phone or "0",
                            Extension=None,
                        ),
                        FaxNumber=None,
                    ),
                    TaxNumber=(
                        payload.shipper.federal_tax_id or payload.shipper.state_tax_id
                    ),
                ),
                ReceiverInformation=ReceiverInformation(
                    Address=Address(
                        Name=payload.recipient.person_name,
                        Company=payload.recipient.company_name,
                        Department=None,
                        StreetNumber="",
                        StreetSuffix=None,
                        StreetName=lib.join(payload.recipient.address_line1, join=True),
                        StreetType=None,
                        StreetDirection=None,
                        Suite=None,
                        Floor=None,
                        StreetAddress2=lib.join(
                            payload.recipient.address_line2, join=True
                        ),
                        StreetAddress3=None,
                        City=payload.recipient.city or "",
                        Province=payload.recipient.state_code or "",
                        Country=payload.recipient.country_code or "",
                        PostalCode=payload.recipient.postal_code or "",
                        PhoneNumber=PhoneNumber(
                            CountryCode=recipient_phone_number.country_code or "0",
                            AreaCode=recipient_phone_number.area_code or "0",
                            Phone=recipient_phone_number.phone or "0",
                            Extension=None,
                        ),
                        FaxNumber=None,
                    ),
                    TaxNumber=(
                        payload.recipient.federal_tax_id
                        or payload.recipient.state_tax_id
                    ),
                ),
                FromOnLabelIndicator=None,
                FromOnLabelInformation=None,
                ShipmentDate=options.shipment_date.state,
                PackageInformation=PackageInformation(
                    ServiceID=service,
                    Description=(
                        packages.description[:25]
                        if any(packages.description or "") else None
                    ),
                    TotalWeight=(
                        TotalWeight(
                            Value=packages.weight.map(
                                provider_units.MeasurementOptions
                            ).LB,
                            WeightUnit=PurolatorWeightUnit.LB.value,
                        )
                        if packages.weight.value
                        else None
                    ),
                    TotalPieces=1,
                    PiecesInformation=ArrayOfPiece(
                        Piece=[
                            Piece(
                                Weight=(
                                    PurolatorWeight(
                                        Value=package.weight.map(
                                            provider_units.MeasurementOptions
                                        ).value,
                                        WeightUnit=PurolatorWeightUnit[
                                            package.weight_unit.value
                                        ].value,
                                    )
                                    if package.weight.value
                                    else None
                                ),
                                Length=(
                                    PurolatorDimension(
                                        Value=package.length.map(
                                            provider_units.MeasurementOptions
                                        ).value,
                                        DimensionUnit=PurolatorDimensionUnit[
                                            package.dimension_unit.value
                                        ].value,
                                    )
                                    if package.length.value
                                    else None
                                ),
                                Width=(
                                    PurolatorDimension(
                                        Value=package.width.map(
                                            provider_units.MeasurementOptions
                                        ).value,
                                        DimensionUnit=PurolatorDimensionUnit[
                                            package.dimension_unit.value
                                        ].value,
                                    )
                                    if package.width.value
                                    else None
                                ),
                                Height=(
                                    PurolatorDimension(
                                        Value=package.height.map(
                                            provider_units.MeasurementOptions
                                        ).value,
                                        DimensionUnit=PurolatorDimensionUnit[
                                            package.dimension_unit.value
                                        ].value,
                                    )
                                    if package.height.value
                                    else None
                                ),
                                Options=None,
                            )
                            for package in packages
                        ]
                    ),
                    DangerousGoodsDeclarationDocumentIndicator=None,
                    OptionsInformation=(
                        ArrayOfOptionIDValuePair(
                            OptionIDValuePair=[
                                OptionIDValuePair(
                                    ID=option.code,
                                    Value=lib.to_money(option.state),
                                )
                                for _, option in options.items()
                            ]
                        )
                        if any(options.items())
                        else None
                    ),
                ),
                InternationalInformation=(
                    InternationalInformation(
                        DocumentsOnlyIndicator=packages.is_document,
                        ContentDetails=(
                            ArrayOfContentDetail(
                                ContentDetail=[
                                    ContentDetail(
                                        Description=(item.description or "")[:25],
                                        HarmonizedCode=item.hs_code or "0000",
                                        CountryOfManufacture=(item.origin_country or payload.shipper.country_code),
                                        ProductCode=item.sku or "0000",
                                        UnitValue=item.value_amount,
                                        Quantity=item.quantity,
                                        NAFTADocumentIndicator=None,
                                        FDADocumentIndicator=None,
                                        FCCDocumentIndicator=None,
                                        SenderIsProducerIndicator=None,
                                        TextileIndicator=None,
                                        TextileManufacturer=None,
                                    )
                                    for item in payload.customs.commodities
                                ]
                            )
                            if not packages.is_document
                            else None
                        ),
                        BuyerInformation=None,
                        PreferredCustomsBroker=None,
                        DutyInformation=DutyInformation(
                            BillDutiesToParty=provider_units.DutyPaymentType.map(
                                payload.customs.duty.paid_by
                            ).value or "Sender",
                            BusinessRelationship=BusinessRelationship.NOT_RELATED.value,
                            Currency=(payload.customs.duty.currency or options.currence.state),
                        ),
                        ImportExportType="Permanent",
                        CustomsInvoiceDocumentIndicator=True,
                    )
                    if is_international
                    else None
                ),
                ReturnShipmentInformation=None,
                PaymentInformation=(
                    PaymentInformation(
                        PaymentType=provider_units.PaymentType[
                            payload.payment.paid_by
                        ].value,
                        RegisteredAccountNumber=(
                            payload.payment.account_number or settings.account_number
                        ),
                        BillingAccountNumber=(
                            payload.payment.account_number or settings.account_number
                        ),
                        CreditCardInformation=None,
                    )
                    if payload.payment is not None
                    else None
                ),
                PickupInformation=PickupInformation(
                    PickupType=PickupType.DROP_OFF.value
                ),
                NotificationInformation=(
                    NotificationInformation(
                        ConfirmationEmailAddress=(
                            options.email_notification_to.state
                            or payload.recipient.email
                        )
                    )
                    if options.email_notification.state
                    and any(
                        [options.email_notification_to.state, payload.recipient.email]
                    )
                    else None
                ),
                TrackingReferenceInformation=(
                    TrackingReferenceInformation(Reference1=payload.reference)
                    if any(payload.reference or "")
                    else None
                ),
                OtherInformation=None,
                ProactiveNotification=None,
            ),
            PrinterType=PrinterType(printing).value,
        ),
    )
    return lib.Serializable(request, provider_utils.standard_request_serializer)


def _create_shipment(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Job:
    return lib.Job(
        id="create",
        data=_shipment_request(payload, settings),
    )


def _get_shipment_label(
    create_response: str,
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Job:
    response = lib.to_element(create_response)
    valid = len(provider_error.parse_error_response(response, settings)) == 0
    shipment_pin = (
        getattr(
            lib.find_element("ShipmentPIN", response, PIN, first=True), "Value", None
        )
        if valid
        else None
    )
    data = (
        documents.get_shipping_documents_request(shipment_pin, payload, settings)
        if valid
        else None
    )

    return lib.Job(id="document", data=data, fallback="")
