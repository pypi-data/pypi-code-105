from ..core.common_utils import get_setting_value


BASE_SHIPPING_API_CODE = 20104000


class ShippingPartnerCodes(object):
    '''ExpressPartner里面要用到的code'''
    # 顺丰
    SF = "sf"
    # 顺丰同城急送
    SFTCJS = "sftcjs"
    # 圆通
    YTO = "yto"
    # 中通
    ZTO = "zto"
    # 申通
    STO = "sto"
    # EMS
    EMS = "ems"
    # 邮政
    YZPY = "yzpy"
    # 韵达
    YD = "yd"
    # 宅急送
    ZJS = "zjs"
    # 京东
    JD = "jd"
    # 德邦
    DBL = "dbl"
    # 百世快递
    HTKY = "htky"
    # 天天
    HHTT = "hhtt"
    # 其它
    OTHERS = "others"
    # 专柜代发
    SHOP = "shop"
    # 闪送
    SS = "ss"


# 快递公司代号与中文对照
ShippingPartnerCodes_DICT = {
    ShippingPartnerCodes.SF: "顺丰",
    ShippingPartnerCodes.SFTCJS: "顺丰同城急送",
    ShippingPartnerCodes.YTO: "圆通",
    ShippingPartnerCodes.ZTO: "中通",
    ShippingPartnerCodes.STO: "申通",
    ShippingPartnerCodes.EMS: "EMS",
    ShippingPartnerCodes.YZPY: "邮政",
    ShippingPartnerCodes.YD: "韵达",
    ShippingPartnerCodes.ZJS: "宅急送",
    ShippingPartnerCodes.JD: "京东",
    ShippingPartnerCodes.DBL: "德邦",
    ShippingPartnerCodes.HTKY: "百世快递",
    ShippingPartnerCodes.HHTT: "天天",
    ShippingPartnerCodes.OTHERS: "其它",
    ShippingPartnerCodes.SHOP: "专柜代发",
    ShippingPartnerCodes.SS: "闪送",
}


class PrintStatus(object):

    NEW = "new"
    PRINTING = "printing"
    PRINTED = "printed"


class SFShippingType(object):

    SF_NEXT_DAY = "sf_next_day"
    SF_THIRD_DAY = "sf_third_day"


class ZTOExpressImportFields(object):
    '''导入中通excel中用的column name'''

    SHIPPING_NUMBER = "shipping_number"
    NOTE = "note"
    POSTAGE = "postage"

    fields = {
        # SHIPPING_NUMBER: '单号',
        SHIPPING_NUMBER: '运单编号',
        POSTAGE: '运费',
        # NOTE: '备注'
        NOTE: '商品信息'
    }


class SFExpressImportFields(object):
    '''导入顺丰excel中用的column name'''

    SHIPPING_NUMBER = "shipping_number"
    NOTE = "note"
    ASSIGNMENT_ID = "assignment_id"
    POSTAGE = "postage"

    fields = {
        SHIPPING_NUMBER: '运单号',
        ASSIGNMENT_ID: '订单号',
        NOTE: '操作备注',
        POSTAGE: "参考运费/元",
    }


# 邮费映射表
EXPRESS_PRICE_MAP = {
    "zto": {
        "北京": 6,
        "天津": 7,
        "河北": 7,
        "甘肃": 15,
        "宁夏": 15,
        "青海": 15,
        "海南": 20,
        "新疆": 20,
        "西藏": 20,
        "default": 8
    }
}


class express_pay_account(object):

    run_env = get_setting_value("RUN_ENV")
    account_tail = ""
    if run_env in ['test', 'unit', 'dev']:
        account_tail = "_测试卡"

    SF_5_DISCOUNT = "顺丰5" + account_tail
    SF_75_DISCOUNT = "顺丰75" + account_tail
    # 买乐 0100283525 五折 |  汉光 0104971724 7.5折
    SF_MAILE = "买乐" + account_tail
    SF_HANGUANG = "顺丰-顺丰速运" + account_tail
    YZPY = "邮政" + account_tail
    BAISHI = "百世海淘代发" + account_tail

    # 当手动填写运单号时, 填充 account
    ARTIFICIAL = "手动填写"

    ACCOUNT_LIST = [
        # {
        #     "express_code": ShippingPartnerCodes.SF,
        #     "express_name": ShippingPartnerCodes_DICT.get(ShippingPartnerCodes.SF),
        #     "name": SF_5_DISCOUNT,
        #     "code": get_setting_value("SF_PAYCARD_NUMBER_5"),
        #     "user_code": get_setting_value("SHIPPING_URL_SF_USERCODE"),
        #     "check_code": get_setting_value("SHIPPING_URL_SF_CHECKCODE")
        # },
        # {
        #     "express_code": ShippingPartnerCodes.SF,
        #     "express_name": ShippingPartnerCodes_DICT.get(ShippingPartnerCodes.SF),
        #     "name": SF_75_DISCOUNT,
        #     "code": get_setting_value("SF_PAYCARD_NUMBER_75"),
        #     "user_code": get_setting_value("SHIPPING_URL_SF_USERCODE"),
        #     "check_code": get_setting_value("SHIPPING_URL_SF_CHECKCODE")
        # },
        {
            "express_code": ShippingPartnerCodes.SF,
            "express_name": ShippingPartnerCodes_DICT.get(ShippingPartnerCodes.SF),
            "name": SF_MAILE,
            "code": get_setting_value("SF_PAYCARD_NUMBER_MAILE"),
            "user_code": get_setting_value("SHIPPING_URL_SF_USERCODE"),
            "check_code": get_setting_value("SHIPPING_URL_SF_CHECKCODE")
        },
        {
            "express_code": ShippingPartnerCodes.SF,
            "express_name": ShippingPartnerCodes_DICT.get(ShippingPartnerCodes.SF),
            "name": SF_HANGUANG,
            "code": get_setting_value("SF_PAYCARD_NUMBER_HANGUANG"),
            "user_code": get_setting_value("SHIPPING_URL_SF_USERCODE"),
            "check_code": get_setting_value("SHIPPING_URL_SF_CHECKCODE")
        },
        {
            "express_code": ShippingPartnerCodes.YZPY,
            "express_name": ShippingPartnerCodes_DICT.get(ShippingPartnerCodes.YZPY),
            "name": YZPY,
            "code": get_setting_value("SHIPPING_CREATE_ORDER_SENDER_NO_YZPY"),
            "ecommerce_no": get_setting_value("SHIPPING_CREATE_ORDER_ECOMMERCE_NO_YZPY"),  # ecCompanyId 电商标识
            "ecCompanyId": get_setting_value("SHIPPING_CREATE_ORDER_ECCOMPANYID_YZPY"),  # ecCompanyId 电商标识
            "sender_no": get_setting_value("SHIPPING_CREATE_ORDER_SENDER_NO_YZPY"),  # sender_no 协议客户代码
            "check_code": get_setting_value("SHIPPING_CREATE_ORDER_SECRET_YZPY"),
        }
    ] if get_setting_value("RUN_ENV") in ['pro'] else [
        # {
        #     "express_code": ShippingPartnerCodes.SF,
        #     "express_name": ShippingPartnerCodes_DICT.get(ShippingPartnerCodes.SF),
        #     "name": SF_5_DISCOUNT,
        #     "code": "7551234567|208",
        #     "user_code": "LJ_8pqmp",
        #     "check_code": "32XbbSfWLlqlXkHqoQJaj5twS24VhnXG"
        # },
        # {
        #     "express_code": ShippingPartnerCodes.SF,
        #     "express_name": ShippingPartnerCodes_DICT.get(ShippingPartnerCodes.SF),
        #     "name": SF_75_DISCOUNT,
        #     "code": "7551234567|1",
        #     "user_code": "LJ_8pqmp",
        #     "check_code": "32XbbSfWLlqlXkHqoQJaj5twS24VhnXG"
        # },
        {
            "express_code": ShippingPartnerCodes.SF,
            "express_name": ShippingPartnerCodes_DICT.get(ShippingPartnerCodes.SF),
            "name": SF_MAILE,
            "code": "7551234567|11",
            "user_code": "0104971724",
            "check_code": "76cjzljvFkW708irQ4VVJMa7cBKpNL7E"
        },
        {
            "express_code": ShippingPartnerCodes.SF,
            "express_name": ShippingPartnerCodes_DICT.get(ShippingPartnerCodes.SF),
            "name": SF_HANGUANG,
            "code": "7551234567|2081",
            "user_code": "0104971724",
            "check_code": "76cjzljvFkW708irQ4VVJMa7cBKpNL7E"
        },
        {
            "express_code": ShippingPartnerCodes.YZPY,
            "express_name": ShippingPartnerCodes_DICT.get(ShippingPartnerCodes.YZPY),
            "name": YZPY,
            "code": get_setting_value("SHIPPING_CREATE_ORDER_SENDER_NO_YZPY"),
            "ecommerce_no": get_setting_value("SHIPPING_CREATE_ORDER_ECOMMERCE_NO_YZPY"),  # ecCompanyId 电商标识
            "ecCompanyId": get_setting_value("SHIPPING_CREATE_ORDER_ECCOMPANYID_YZPY"),  # ecCompanyId 电商标识
            "sender_no": get_setting_value("SHIPPING_CREATE_ORDER_SENDER_NO_YZPY"),  # sender_no 协议客户代码
            "check_code": get_setting_value("SHIPPING_CREATE_ORDER_SECRET_YZPY"),
        }
    ]

    ACCOUNT_NAME_2_CODE_MAP = {account_item["name"]: account_item["express_code"] + "," + account_item["code"] for account_item in ACCOUNT_LIST}
    ACCOUNT_CODE_2_NAME_MAP = {account_item["code"]: account_item["name"] for account_item in ACCOUNT_LIST}
    ACCOUNT_NAME_2_DICT_MAP = {account_item["name"]: account_item for account_item in ACCOUNT_LIST}


class express_pay_method(object):
    # 寄付
    SENDER_PAY = "sender_pay"
    # 到付
    RECEIVER_PAY = "receiver_pay"

    EXPRESS_PAY_METHOD_CHOISE = (
        (SENDER_PAY, "寄付"),
        (RECEIVER_PAY, "到付"),
    )
