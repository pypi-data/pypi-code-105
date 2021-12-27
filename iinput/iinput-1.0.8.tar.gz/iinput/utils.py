

def isfloat(s):
    if '.' not in s:
        return False
    try:
        float(s)
        return True
    except ValueError:
        return False


def isint(s):
    return s.strip().lstrip("-+").isdigit()


def ischar(v):
    return type(v) == str and len(v) == 1


def interpret_type(s):
    s = s.strip()
    if s.lower() in ["true", "false"]:
        return bool
    elif isint(s):
        return int
    elif isfloat(s):
        return float
    elif s == "None":
        return None
    elif s:
        return str 
    else:
        return None


def auto_cast(items, allowed_types):
    for i in range(len(items)):
        items[i] = items[i].strip()
        item_type = interpret_type(items[i])
        if item_type not in allowed_types:
            if items[i] in ['0', '1'] and bool in allowed_types:
                items[i] = items[i] == '1'
            elif items[i] and str in allowed_types:
                items[i] = str(items[i])
            else:
                items[i] = None
        elif item_type == bool:
            items[i] = items[i].lower() == "true"
        else:
            items[i] = item_type(items[i])
    return items


def split_ws(string, delimiter):
    values = [v.strip() for v in string.split(delimiter) if v.strip()]
    return values
