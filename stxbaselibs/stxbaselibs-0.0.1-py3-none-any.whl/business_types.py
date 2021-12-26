
class BaseDomainModel(object):

    def __new__(cls, *args, **kwargs):
        for key in dir(cls):
            if not key.startswith('_'):
                setattr(cls, f"_{key}", getattr(cls, key))
                field_attr = getattr(cls, f"_{key}")
                setattr(cls, key, property(
                    getattr(field_attr, key, field_attr.get_Value),
                    getattr(field_attr, key, field_attr.set_Value),
                ))
        instance = super(BaseDomainModel, cls).__new__(cls, *args, **kwargs)
        return instance


class BaseField(object):
    default_validators = []

    def __init__(self):
        self.value = None

    def get_Value(self, _parent_obj):
        return self.value

    def set_Value(self, _parent_obj, _value):
        for validator in self.default_validators:
            validator(_value)

        self.value = _value
