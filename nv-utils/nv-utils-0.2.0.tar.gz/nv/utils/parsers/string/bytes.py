from typing import Union

try:
    import chardet
except ModuleNotFoundError:
    chardet = None


from ..parser import RAISE_IF_UNKNOWN


def cast_bytes(obj: Union[bytes, bytearray], fallback_encoding=None, default=RAISE_IF_UNKNOWN) -> str:
    encoding = chardet.detect(obj).get('encoding', fallback_encoding) if chardet else fallback_encoding

    if encoding is None:
        if default is RAISE_IF_UNKNOWN:
            raise UnicodeError(f"Unable to decode {type(obj)} object and no fallback_encoding provided")
        return default

    try:
        return obj.decode(encoding=encoding)
    except UnicodeError as exc:
        if default is RAISE_IF_UNKNOWN:
            raise exc
        return default
