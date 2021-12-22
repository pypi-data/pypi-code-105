# pylint: disable=too-many-branches
# pylint: disable=unused-import
# pylint: disable=line-too-long
# pylint: disable=consider-using-from-import


import utils.dict as dictionary_utils
import colemen_object_utils as cou


def keys_to_lower(dictionary):
    '''
        Converts all keys in a dictionary to lowercase.

        ----------

        Arguments
        -------------------------
        `dictionary` {dict}
            The dictionary whose keys will be formatted

        Return {dict|None}
        ----------------------
        The formatted dictionary upon success, None otherwise

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-22-2021 08:22:40
        `memberOf`: dict
        `version`: 1.0
        `method_name`: keys_to_lower
    '''
    # pylint: disable=isinstance-second-argument-not-valid-type
    if isinstance(dictionary, (dict)) is False:
        print(f"Value provided is not a dictionary: {type(dictionary)}")
        return None
    return {k.lower(): v for k, v in dictionary.items()}


def set_defaults(defaults, obj):
    '''
        Sets default values on the obj provided, if they are not already set.

        ----------

        Arguments
        -------------------------
        `defaults` {dict}
            A dictionary of default values to assign if they are missing in the obj
        `obj` {dict}
            The dictionary to set the default values on.

        Return {dict|None}
        ----------------------
        The obj dictionary with default values assigned.\n
        None if there is an error.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-22-2021 08:32:26
        `memberOf`: dict
        `version`: 1.0
        `method_name`: set_defaults
    '''
    if isinstance(defaults, (dict)) is False:
        print(f"defaults provided must be a dictionary: {type(defaults)}")
        return None
    if isinstance(obj, (dict)) is False:
        print(f"obj provided must be a dictionary: {type(obj)}")
        return None

    for key, value in defaults.items():
        if key not in obj:
            obj[key] = value
    return obj


def get_unique_keys(obj, **kwargs):
    '''
        Gets all unique keys in the dictionary provided.

        ----------

        Arguments
        -------------------------
        `obj` {dict|list}
            The object or list to search for keys within.

        Keyword Arguments
        -------------------------
        [`sort_list`=True] {bool}
            Sort the list alphabetically.
        [`case_sensitive`=True] {bool}
            If True the case of the key is ignored.
        [`force_lowercase`=True] {bool}
            Convert all keys to lowercase.
        [`recursive`=True] {bool}
            Recurse into nested objects to find keys.
        [`max_depth`=500] {int}
            The maximum recursions it is allowed to make.

        Return {list}
        ----------------------
        A list of unique keys from the object, if none are found the list is empty.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-22-2021 08:40:14
        `memberOf`: dict
        `version`: 1.0
        `method_name`: get_unique_keys
    '''
    __current_depth = cou.get_kwarg(['__current_depth'], 0, int, **kwargs)
    sort_list = cou.get_kwarg(['sort_list'], False, bool, **kwargs)
    case_sensitive = cou.get_kwarg(['case_sensitive'], True, bool, **kwargs)
    force_lowercase = cou.get_kwarg(['force_lowercase'], True, bool, **kwargs)
    recursive = cou.get_kwarg(['recursive'], True, bool, **kwargs)
    max_depth = cou.get_kwarg(['max_depth'], 500, int, **kwargs)
    kwargs['__current_depth'] = __current_depth + 1

    keys = []

    if recursive is True and __current_depth < max_depth:
        if isinstance(obj, (list, tuple, set)):
            for element in obj:
                if isinstance(element, (list, dict)):
                    keys = keys + get_unique_keys(element, **kwargs)

    if isinstance(obj, dict):
        keys = list(obj.keys())

        if recursive is True and __current_depth < max_depth:
            # pylint: disable=unused-variable
            for k, value in obj.items():
                # find nested objects
                if isinstance(value, (list, dict, tuple, set)):
                    keys = keys + get_unique_keys(value, **kwargs)

    if case_sensitive is True:
        output = []
        lkkeys = []
        for key in keys:
            low_key = key.lower()
            if low_key not in lkkeys:
                output.append(key)
                lkkeys.append(low_key)
        keys = output

    if force_lowercase is True:
        keys = [x.lower() for x in keys]

    keys = list(set(keys))

    if sort_list is True:
        keys = sorted(keys, key=lambda x: int("".join([i for i in x if i.isdigit()])))
    return keys
