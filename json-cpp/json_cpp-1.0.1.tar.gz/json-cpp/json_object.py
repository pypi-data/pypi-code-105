import json
from .util import check_type


class JsonObject:
    def __str__(self):
        s = ""
        v = vars(self)
        for k in v:
            if k[0] == "_":
                continue
            if s:
                s += ","
            s += "\"%s\":" % k
            if isinstance(v[k], str):
                s += "%s" % json.dumps(v[k])
            elif isinstance(v[k], bool):
                s += "%s" % str(v[k]).lower()
            else:
                s += "%s" % str(v[k])
        return "{%s}" % s

    def __eq__(self, other):
        if type(self) is not type(other):
            return False
        v = vars(self)
        vo = vars(other)
        for k in v:
            if k[0] == "_":
                continue
            if v[k] != vo[k]:
                return False
        return True

    def copy(self):
        return type(self).parse(str(self))

    def format(self, format_string):
        check_type(format_string, str, "wrong type for format_string")
        v = vars(self)
        for k in v:
            if not isinstance(v[k], JsonObject):
                continue
            pos = format_string.find("{"+k+":")
            if pos >= 0:
                sub_format_start = format_string.find(":", pos) + 1
                sub_format_end = sub_format_start
                bracket_count = 1
                while bracket_count and sub_format_end < len(format_string):
                    c = format_string[sub_format_end]
                    if c == '{':
                        bracket_count += 1
                    if c == '}':
                        bracket_count -= 1
                    sub_format_end += 1
                sub_format = format_string[sub_format_start:sub_format_end-1]
                sub_str = v[k].format(sub_format)
                format_string = format_string[:pos] + sub_str + format_string[sub_format_end:]
        return format_string.format(**vars(self))

    @classmethod
    def bar(cls):
        print(type(cls))
        print(cls)
        print(isinstance(cls, JsonObject))

    @classmethod
    def parse(cls, json_string="", json_dictionary=None):
        if json_string:
            check_type(json_string, str, "wrong type for json_string")
            json_dictionary = json.loads(json_string)

        check_type(json_dictionary, dict, "wrong type for json_dictionary")
        new_object = cls()
        for key in json_dictionary:
            it = type(getattr(new_object, key))
            if issubclass(it, JsonObject):
                av = it.parse(json_dictionary=json_dictionary[key])
            elif issubclass(it, JsonList):
                av = it.parse(json_list=json_dictionary[key])
            else:
                av = it(json_dictionary[key])
            setattr(new_object, key, av)
        return new_object


class JsonList(list):

    def __init__(self, iterable=None, list_type=None):
        iterable = list() if not iterable else iterable
        iter(iterable)
        map(self._typeCheck, iterable)
        list.__init__(self, iterable)
        self.list_type = list_type


    def _typeCheck(self, val):
        check_type(val, self.list_type, "Wrong type %s, this list can hold only instances of %s" % (type(val), str(self.list_type)))

    def __iadd__(self, other):
        map(self._typeCheck, other)
        list.__iadd__(self, other)
        return self

    def __add__(self, other):
        iterable = [item for item in self] + [item for item in other]
        return JsonList(iterable, self._allowedType)

    def __radd__(self, other):
        iterable = [item for item in other] + [item for item in self]
        if isinstance(other, JsonList):
            return self.__class__(iterable, other.list_type)
        return JsonList(iterable, self.list_type)

    def __setitem__(self, key, value):
        itervalue = (value,)
        if isinstance(key, slice):
            iter(value)
            itervalue = value
        map(self._typeCheck, itervalue)
        list.__setitem__(self, key, value)

    def __setslice__(self, i, j, iterable):
        iter(iterable)
        map(self._typeCheck, iterable)
        list.__setslice__(self, i, j, iterable)

    def append(self, val):
        self._typeCheck(val)
        list.append(self, val)

    def extend(self, iterable):
        iter(iterable)
        map(self._typeCheck, iterable)
        list.extend(self, iterable)

    def insert(self, i, val):
        self._typeCheck(val)
        list.insert(self, i, val)

    def __str__(self):
        return "[" + ",".join([str(x) for x in self]) + "]"

    def get(self, m):
        it = type(vars(self.list_type)[m])
        l = JsonList(list_type=it)
        for i in self:
            l.append(vars(i)[m])
        return l

    def where(self, m, v, o="=="):
        nl = type(self)()
        for i in self:
            if type(vars(i)[m]) is str or issubclass(type(vars(i)[m]), JsonObject):
                e = "'%s' %s '%s'" % (str(vars(i)[m]), o, str(v))
            else:
                e = "%s %s %s" % (str(vars(i)[m]), o, str(v))
            if eval(e):
                nl.append(i)
        return nl

    def copy(self):
        return type(self).parse(str(self))

    @classmethod
    def parse(cls, json_string="", json_list=None):
        if json_string:
            check_type(json_string, str, "wrong type for json_string")
            json_list = json.loads(json_string)
        check_type(json_list, list, "wrong type for json_list")
        new_list = cls()
        it = new_list.list_type
        ic = it().__class__
        for i in json_list:
            if issubclass(ic, JsonObject):
                new_list.append(it.parse(json_dictionary=i))
            elif issubclass(ic, JsonList):
                new_list.append(it.parse(json_list=i))
            else:
                new_list.append(i)
        return new_list
