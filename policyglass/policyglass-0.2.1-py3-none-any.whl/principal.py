"""Principal classes."""
import json
import re
from typing import Dict, List, Optional

from pydantic import BaseModel

from .effective_arp import EffectiveARP


class PrincipalType(str):
    """A principal type, e.g. Federated or AWS.

    See `AWS JSON policy elements: Principal
    <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_principal.html>`__
    for more.
    """


class PrincipalValue(str):
    """An ARN, wildcard, or other appropriate value of a policy Principal.

    See `AWS JSON policy elements: Principal
    <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_principal.html>`__
    for more.
    """


class PrincipalCollection(Dict[PrincipalType, List[PrincipalValue]]):
    """A collection of Principals of different types, unique to PolicyGlass."""

    @property
    def principals(self) -> List["Principal"]:
        result = []
        for principal_type, principal_values in self.items():
            for principal_value in principal_values:
                result.append(Principal(principal_type, principal_value))
        return result

    def __hash__(self) -> int:  # type: ignore[override]
        """Generate a hash for this principal."""
        return hash(json.dumps({"candidate": 5, "data": 1}, sort_keys=True))

    def __lt__(self, other: object) -> bool:
        """There are few scenarios in which a Principal can be said to contain another object.

        "You cannot use a wildcard to match part of a principal name or ARN."
        `AWS JSON policy elements: Principal
        <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_principal.html>`__

        You can however use *just* a wildcard to match a whole principal.
        An ``arn:aws:iam::123456789012:root`` ARN also matches every principal in that account.

        Parameters:
            other: The object to see if this principal contains.
        """
        return False

    def __contains__(self, other: object) -> bool:
        """Not Implemented.

        Parameters:
            other: The object to see if this object contains.

        Raises:
            NotImplementedError: This method is not implemented.
        """
        raise NotImplementedError()


class Principal(BaseModel):
    """A class which represents a single Principal including its type.

    Objects of this type are typically generated by the :class:`~policyglass.statement.Statement` class.
    """

    #: Principal Type
    type: PrincipalType
    #: Principal value
    value: PrincipalValue

    def __init__(self, type: PrincipalType, value: PrincipalValue) -> None:
        super().__init__(
            type=type,
            value=self._normalize_account_id(value),
        )

    def issubset(self, other: object) -> bool:
        """Whether this object contains all the elements of another object (i.e. is a subset of the other object).

        Parameters:
            other: The object to determine if our object contains.

        Raises:
            ValueError: If the other object is not of the same type as this object.
        """
        if not isinstance(other, self.__class__):
            raise ValueError(f"Cannot compare {self.__class__.__name__} and {other.__class__.__name__}")
        if self.type != other.type:
            return False
        if other.value == "*":
            return True
        if other.is_account and self.account_id == other.account_id:
            return True
        for self_element, other_element in zip(self.arn_elements, other.arn_elements):
            if self_element != other_element and other_element:
                return False
        return True

    @property
    def account_id(self) -> Optional[str]:
        """Return the account id of this Principal if there is one."""
        try:
            return self.arn_elements[4]
        except IndexError:
            return None

    @property
    def arn_elements(self) -> List[str]:
        """Return a list of arn elements, replacing blanks with ``""``."""
        return [element or "" for element in self.value.split(":")]

    @property
    def is_account(self) -> bool:
        """Return true if the prinncipal is an account."""
        return bool(self.type == "AWS" and re.match(r"^arn:aws:iam::\d+:root$", self.value))

    @staticmethod
    def _normalize_account_id(value: PrincipalValue) -> PrincipalValue:
        """Return a fully qualified account id if a value is a short account id.

        Parameters:
            value: The value to normalize.
        """
        if re.match(r"^\d+$", value):
            return PrincipalValue(f"arn:aws:iam::{value}:root")
        return PrincipalValue(value)

    def __eq__(self, other: object) -> bool:
        """Whether this object contains (but is not equal to) another object.

        Parameters:
            other: The object to determine if our object contains.

        Raises:
            ValueError: If the other object is not of the same type as this object.
        """
        if not isinstance(other, self.__class__):
            raise ValueError(f"Cannot compare {self.__class__.__name__} and {other.__class__.__name__}")
        return self.type == other.type and self.value == other.value

    def __lt__(self, other: object) -> bool:
        """Whether this object contains (but is not equal to) another object.

        Parameters:
            other: The object to determine if our object contains.

        Raises:
            ValueError: If the other object is not of the same type as this object.
        """
        if not isinstance(other, self.__class__):
            raise ValueError(f"Cannot compare {self.__class__.__name__} and {other.__class__.__name__}")
        if self == other:
            return False
        return self.issubset(other)

    def __repr__(self) -> str:
        """Return an insantiable representation of this object."""
        return f"{self.__class__.__name__}(type='{self.type}', value='{self.value}')"

    def __hash__(self) -> int:
        """Return a hash representation of this object."""
        return hash(str(self))


class EffectivePrincipal(EffectiveARP[Principal]):
    """EffectivePrincipals are the representation of the difference between an Principal and its exclusion.

    The allowed Principal is the difference (subtraction) of the excluded Principals
    from the included Principal.
    """

    _arp_type = Principal
