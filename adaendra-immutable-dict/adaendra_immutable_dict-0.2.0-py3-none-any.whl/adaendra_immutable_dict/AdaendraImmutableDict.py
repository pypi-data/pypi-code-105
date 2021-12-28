from copy import deepcopy


class AdaendraImmutableDict(dict):
    r"""
    Class to create an immutable dictionary.

    It works as same as `dict`, without methods that can change the
    immutability. In addition, it supports __hash__().
    
    :param dict: dict - The dictionary to set as immutable.
    """

    # Little trick to save RAM -> https://book.pythontips.com/en/latest/__slots__magic.html
    __slots__ = (
        "_hash",
    )

    def __init__(self, *args, **kwargs):
        pass

    def __hash__(self, *args, **kwargs):
        r"""
        Calculates the hash if all values are hashable, otherwise raises a 
        TypeError.
        """
        if self._hash is not None:
            _hash = self._hash
        else:
            try:
                fs = frozenset(self.items())
            except TypeError:
                _hash = -1
            else:
                _hash = hash(fs)

            object.__setattr__(self, "_hash", _hash)

        if _hash == -1:
            raise TypeError("Not all values are hashable.")

        return _hash

    def __repr__(self, *args, **kwargs):
        r"""
        Identical to dict.__repr__().
        Represent the class object as a String.

        Format : <Class Name>(<Body>)
        """
        class_name = self.__class__.__name__
        body = super().__repr__(*args, **kwargs)

        return f"{class_name}({body})"

    def copy(self):
        r"""
        Return the object itself, as it's an immutable.
        """
        return self

    def __copy__(self, *args, **kwargs):
        r"""
        See copy().
        """
        return self.copy()

    def __deepcopy__(self, *args, **kwargs):
        r"""
        As for tuples, if hashable, see copy(); otherwise, it returns a 
        deepcopy.
        """
        try:
            hash(self)
        except TypeError:
            tmp_deep_copy = deepcopy(dict(self))

            return self.__class__(tmp_deep_copy)

        return self.__copy__(*args, **kwargs)

    def __reduce__(self, *args, **kwargs):
        """
        Unsupported method, will raise a TypeError.
        :raise: TypeError
        """
        raise TypeError(
            f"'{self.__class__.__name__}' object doesn't support item update"
        )

    def __setitem__(self, key, val, *args, **kwargs):
        """
        Unsupported method, will raise a TypeError.
        :raise: TypeError
        """
        raise TypeError(
            f"'{self.__class__.__name__}' object doesn't support item assignment"
        )

    def __delitem__(self, key, *args, **kwargs):
        """
        Unsupported method, will raise a TypeError.
        :raise: TypeError
        """
        raise TypeError(
            f"'{self.__class__.__name__}' object doesn't support item deletion"
        )

    # Decorator to let know that this method is available for the static object and all its instances.
    # More info : https://www.programiz.com/python-programming/methods/built-in/classmethod
    @classmethod
    def fromkeys(cls, *args, **kwargs):
        r"""
        Use the method dict.fromkeys and take the result to generate the Immutable Dict.
        :param cls: Class - Class where the methode is defined in.
        :return: AdaendraImmutableDict.
        """
        return cls(dict.fromkeys(*args, **kwargs))


def immutable(self, *args, **kwargs):
    """
    Function for not implemented method since the object is immutable.
    :param self: The immutable object which has an update function called.
    :raise: AttributeError - Raised when the method is called.
    """
    raise AttributeError(f"'{self.__class__.__name__}' object is read-only")


def AdaendraImmutableDict_or(self, other, *args, **kwargs):
    """
    Override of the function OR for AdaendraImmutableDict.
    :param self: First AdaendraImmutableDict to compare.
    :param other: Second AdaendraImmutableDict to compare.
    :return: AdaendraImmutableDict - The first AdaendraImmutableDict will be return without modifications.
    """
    return self


# ----- Overrides ----- #
# OR operator
AdaendraImmutableDict.__or__ = AdaendraImmutableDict_or

# In place operator : https://docs.python.org/3/library/operator.html#in-place-operators
AdaendraImmutableDict.__ior__ = AdaendraImmutableDict_or

# Various dict methods
AdaendraImmutableDict.clear = immutable
AdaendraImmutableDict.pop = immutable
AdaendraImmutableDict.popitem = immutable
AdaendraImmutableDict.setdefault = immutable
AdaendraImmutableDict.update = immutable
AdaendraImmutableDict.__delattr__ = immutable
AdaendraImmutableDict.__setattr__ = immutable


def AdaendraImmutableDict_new(cls, *args, **kwargs):
    """
    Method to create a new AdaendraImmutableDict.
    """
    has_kwargs = bool(kwargs)
    continue_creation = True

    # Do some checks to avoid to create an AdaendraImmutableDict from another AdaendraImmutableDict.
    if len(args) == 1 and not has_kwargs:
        it = args[0]

        if it.__class__ == AdaendraImmutableDict and cls == AdaendraImmutableDict:
            self = it
            continue_creation = False

    # If it's not a AdaendraImmutableDict inception
    if continue_creation:
        self = dict.__new__(cls, *args, **kwargs)
        dict.__init__(self, *args, **kwargs)
        object.__setattr__(self, "_hash", self.__hash__)

    return self


AdaendraImmutableDict.__new__ = AdaendraImmutableDict_new

__all__ = (AdaendraImmutableDict.__name__,)
