import bson
from decimal import Decimal

def chunk_list(values: list, num: int):
    for i in range(0, len(values), num):
        yield values[i: i+num]

#转换类为字典
def convert_class_to_dict(obeject_class):
    object_value = {}
    for key in dir(obeject_class):
        value = getattr(obeject_class, key)
        if not key.startswith('__') and not key.startswith('_') and not callable(value):
            object_value[key] = value
    return object_value

def generate_object_id():
    return bson.ObjectId().__str__()

def remove_exponent(value: Decimal):
    return value.to_integral() if value == value.to_integral() else value.normalize()

def format_value(value: str, scale: str, decimal: int = 2) -> str:
    value = str(value)
    scale = str(scale)
    if len(value) > 0:
        try:
            if value.lower() == 'true':
                value = '1'
            elif value.lower() == 'false':
                value = '0'
            value = float(value)
            if scale != '1':
                value = value * float(scale)
            format = f"%.{decimal}f"

            value = format % value  # 格式化小数点
            value = remove_exponent(Decimal(value))
        except Exception as e:
            pass
    return str(value)


