"""Declares :class:`BaseSchema`."""
import marshmallow.fields


class BaseSchema:
    id = marshmallow.fields.UUID(
        required=True
    )

    code = marshmallow.fields.String(
        required=True
    )

    message = marshmallow.fields.String(
        required=True
    )

    detail = marshmallow.fields.String(
        required=False
    )

    hint = marshmallow.fields.String(
        required=False
    )

    backoff = marshmallow.fields.Dict(
        required=False
    )

    def dump(self, *args, **kwargs) -> dict:
        return {
            k: v for k, v in dict.items(super().dump(*args, **kwargs))
            if v is not None
        }
