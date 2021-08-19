from purplship.core.utils import Enum, Flag, Spec
from purplship.core.units import PackagePreset

PRESET_DEFAULTS = dict(dimension_unit="IN", weight_unit="LB")


class PackagePresets(Flag):
    ups_small_express_box = PackagePreset(
        **dict(weight=30.0, width=13.0, height=11.0, length=2.0),
        **PRESET_DEFAULTS
    )
    ups_medium_express_box = PackagePreset(
        **dict(weight=30.0, width=16.0, height=11.0, length=3.0),
        **PRESET_DEFAULTS
    )
    ups_large_express_box = PackagePreset(
        **dict(weight=30.0, width=18.0, height=13.0, length=3.0),
        **PRESET_DEFAULTS
    )
    ups_express_tube = PackagePreset(
        **dict(width=38.0, height=6.0, length=6.0),
        **PRESET_DEFAULTS
    )
    ups_express_pak = PackagePreset(
        **dict(width=16.0, height=11.75, length=1.5),
        **PRESET_DEFAULTS
    )
    ups_world_document_box = PackagePreset(
        **dict(width=17.5, height=12.5, length=3.0),
        **PRESET_DEFAULTS
    )


class LabelType(Flag):
    PDF_6x4 = ('GIF', 6, 4)
    PDF_8x4 = ('GIF', 8, 4)
    ZPL_6x4 = ('ZPL', 6, 4)

    """ Unified Label type mapping """
    PDF = PDF_6x4
    ZPL = ZPL_6x4


class Incoterm(Enum):
    CFR = "Cost and Freight"
    CIF = "Cost Insurance and Freight"
    CIP = "Carriage and Insurance Paid"
    CPT = "Carriage Paid To"
    DAF = "Delivered at Frontier"
    DDP = "Delivery Duty Paid"
    DDU = "Delivery Duty Unpaid"
    DEQ = "Delivered Ex Quay"
    DES = "Delivered Ex Ship"
    EXW = "Ex Works"
    FAS = "Free Alongside Ship"
    FCA = "Free Carrier"
    FOB = "Free On Board"


class WeightUnit(Enum):
    KG = "KGS"
    LB = "LBS"


class FreightPackagingType(Flag):
    ups_freight_bag = "BAG"
    ups_freight_bale = "BAL"
    ups_freight_barrel = "BAR"
    ups_freight_bundle = "BDL"
    ups_freight_bin = "BIN"
    ups_freight_box = "BOX"
    ups_freight_basket = "BSK"
    ups_freight_bunch = "BUN"
    ups_freight_cabinet = "CAB"
    ups_freight_can = "CAN"
    ups_freight_carrier = "CAR"
    ups_freight_case = "CAS"
    ups_freight_carboy = "CBY"
    ups_freight_container = "CON"
    ups_freight_crate = "CRT"
    ups_freight_cask = "CSK"
    ups_freight_carton = "CTN"
    ups_freight_cylinder = "CYL"
    ups_freight_drum = "DRM"
    ups_freight_loose = "LOO"
    ups_freight_other = "OTH"
    ups_freight_pail = "PAL"
    ups_freight_pieces = "PCS"
    ups_freight_package = "PKG"  # equivalent of user custom packaging
    ups_freight_pipe_line = "PLN"
    ups_freight_pallet = "PLT"
    ups_freight_rack = "RCK"
    ups_freight_reel = "REL"
    ups_freight_roll = "ROL"
    ups_freight_skid = "SKD"
    ups_freight_spool = "SPL"
    ups_freight_tube = "TBE"
    ups_freight_tank = "TNK"
    ups_freight_unit = "UNT"
    ups_freight_van_pack = "VPK"
    ups_freight_wrapped = "WRP"

    """ unified Packaging type mapping  """
    envelope = ups_freight_other
    pak = ups_freight_other
    tube = ups_freight_cylinder
    pallet = ups_freight_pallet
    small_box = ups_freight_box
    medium_box = ups_freight_box
    your_packaging = ups_freight_box


class PackagingType(Flag):
    ups_unknown = "00"
    ups_letter = "01"
    ups_customer_supplied_package = "02"
    ups_tube = "03"
    ups_pak = "04"
    ups_ups_express_box = "21"
    ups_ups_25_kg_box = "24"
    ups_ups_10_kg_box = "25"
    ups_pallet = "30"
    ups_small_express_box = "2a"
    ups_medium_express_box = "2b"
    ups_large_express_box = "2c"
    ups_flats = "56"
    ups_parcels = "57"
    ups_bpm = "58"
    ups_first_class = "59"
    ups_priority = "60"
    ups_machineables = "61"
    ups_irregulars = "62"
    ups_parcel_post = "63"
    ups_bpm_parcel = "64"
    ups_media_mail = "65"
    ups_bpm_flat = "66"
    ups_standard_flat = "67"

    """ unified Packaging type mapping  """
    envelope = ups_letter
    pak = ups_pak
    tube = ups_tube
    pallet = ups_pallet
    small_box = ups_small_express_box
    medium_box = ups_medium_express_box
    your_packaging = ups_customer_supplied_package


class FreightServiceCode(Enum):
    ups_freight_ltl = "308"
    ups_freight_ltl_guaranteed = "309"
    ups_freight_ltl_guaranteed_am = "334"
    ups_standard_ltl = "349"


class ServiceCode(Enum):
    ups_standard = "11"
    ups_worldwide_expedited = "08"
    ups_worldwide_express = "07"
    ups_worldwide_express_plus = "54"
    ups_worldwide_saver = "65"
    ups_2nd_day_air = "02"
    ups_2nd_day_air_am = "59"
    ups_3_day_select = "12"
    ups_expedited_mail_innovations = "M4"
    ups_first_class_mail = "M2"
    ups_ground = "03"
    ups_next_day_air = "01"
    ups_next_day_air_early = "14"
    ups_next_day_air_saver = "13"
    ups_priority_mail = "M3"
    ups_expedited = "02"
    ups_express_saver_ca = "13"
    ups_access_point_economy = "70"
    ups_express = "01"
    ups_express_early_ca = "14"
    ups_express_saver = "65"
    ups_express_early = "54"
    ups_expedited_eu = "08"
    ups_express_eu = "07"
    ups_express_plus = "54"
    ups_today_dedicated_courier = "83"
    ups_today_express = "85"
    ups_today_express_saver = "86"
    ups_today_standard = "82"
    ups_worldwide_express_freight = "96"
    ups_priority_mail_innovations = "M5"
    ups_economy_mail_innovations = "M6"


class ServiceOption(Enum):
    ups_negotiated_rates_indicator = Spec.asFlag("NegotiatedRatesIndicator")
    ups_frs_shipment_indicator = Spec.asFlag("FRSShipmentIndicator")
    ups_rate_chart_indicator = Spec.asFlag("RateChartIndicator")
    ups_user_level_discount_indicator = Spec.asFlag("UserLevelDiscountIndicator")
    ups_saturday_delivery_indicator = Spec.asFlag("SaturdayDeliveryIndicator")
    ups_access_point_cod = Spec.asValue("AccessPointCOD", float)
    ups_deliver_to_addressee_only_indicator = Spec.asFlag("DeliverToAddresseeOnlyIndicator")
    ups_direct_delivery_only_indicator = Spec.asFlag("DirectDeliveryOnlyIndicator")
    ups_cod = Spec.asValue("COD", float)
    ups_delivery_confirmation = Spec.asFlag("DeliveryConfirmation")
    ups_return_of_document_indicator = Spec.asFlag("ReturnOfDocumentIndicator")
    ups_carbonneutral_indicator = Spec.asFlag("UPScarbonneutralIndicator")
    ups_certificate_of_origin_indicator = Spec.asFlag("CertificateOfOriginIndicator")
    ups_pickup_options = Spec.asFlag("PickupOptions")
    ups_delivery_options = Spec.asFlag("DeliveryOptions")
    ups_restricted_articles = Spec.asFlag("RestrictedArticles")
    ups_shipper_export_declaration_indicator = Spec.asFlag("ShipperExportDeclarationIndicator")
    ups_commercial_invoice_removal_indicator = Spec.asFlag("CommercialInvoiceRemovalIndicator")
    ups_import_control = Spec.asFlag("ImportControl")
    ups_return_service = Spec.asFlag("ReturnService")
    ups_sdl_shipment_indicator = Spec.asFlag("SDLShipmentIndicator")
    ups_epra_indicator = Spec.asFlag("EPRAIndicator")

    """ Unified Option type mapping """
    cash_on_delivery = ups_cod


class FreightClass(Enum):
    ups_freight_class_50 = 50
    ups_freight_class_55 = 55
    ups_freight_class_60 = 60
    ups_freight_class_65 = 65
    ups_freight_class_70 = 70
    ups_freight_class_77_5 = 77.5
    ups_freight_class_85 = 85
    ups_freight_class_92_5 = 92.5
    ups_freight_class_100 = 100
    ups_freight_class_110 = 110
    ups_freight_class_125 = 125
    ups_freight_class_150 = 150
    ups_freight_class_175 = 175
    ups_freight_class_200 = 200
    ups_freight_class_250 = 250
    ups_freight_class_300 = 300
    ups_freight_class_400 = 400
    ups_freight_class_500 = 500
