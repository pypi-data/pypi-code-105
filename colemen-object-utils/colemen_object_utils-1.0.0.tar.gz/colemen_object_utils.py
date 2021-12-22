# pylint: disable=too-many-branches
# pylint: disable=unused-import
# pylint: disable=line-too-long

import colemen_string_utils as strUtils
import utils.dict as dictionary


def get_kwarg(key_name, default_val=False, value_type=None, **kwargs):
    '''
        Gets a kwarg from the options provided that is of the correct type.

        ----------

        Arguments
        -------------------------
        `key_name` {str|list}
            The name or list of names that the kwarg can match.
        [`default_val`=False] {mixed}
            The default value to return if the key is not found.
        [`value_type`=None] {type|tuple}
            The type or a tuple of types that the kwarg value must match.
        `kwargs` {mixed}
            The **kwargs value that will be searched

        Return {mixed}
        ----------------------
        The kwarg value, if it can be found.
        The default value, if it cannot be found.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-22-2021 08:26:01
        `memberOf`: colemen_object_utils
        `version`: 1.0
        `method_name`: get_kwarg
    '''
    kwargs = dictionary.keys_to_lower(kwargs)
    if isinstance(key_name, list) is False:
        key_name = [key_name]

    for name in key_name:
        # generate basic variations of the name
        varis = strUtils.gen.variations(name)
        for v_name in varis:
            if v_name in kwargs:
                if value_type is not None:
                    if isinstance(kwargs[v_name], value_type) is True:
                        return kwargs[v_name]
                else:
                    return kwargs[v_name]
    return default_val
