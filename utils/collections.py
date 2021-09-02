from collections import UserDict
from enum import Enum
from typing import Any, List, Type

from utils.constants import NOT_SET
from utils.exceptions import MissingKeys


class Mapping(UserDict):
    """
    Dictionary that allows you to specify a default value.

    If valid_keys is specified, it will only return the default value for keys in that
    list, raising an exception if key is neither in the dict or in the valid_keys list.
    """

    empty_value = NOT_SET

    def __init__(
        self,
        values: dict,
        valid_keys: List[str] = None,
        default_value: Any = empty_value,
        read_only=False,
    ):
        super().__init__()
        self.data = dict(values)
        self.valid_keys = valid_keys
        self.default_value = default_value
        self._read_only = read_only

    def has_default_value(self) -> bool:
        return self.default_value is not self.empty_value

    def key_in_valid_keys(self, key) -> bool:
        if self.valid_keys is None:
            return True

        return key in self.valid_keys

    def __missing__(self, key):
        if not self.has_default_value() or not self.key_in_valid_keys(key):
            raise KeyError(key)

        return self.default_value

    def __setitem__(self, key, value):
        if self._read_only:
            raise AttributeError("This class is read only")

        super().__setattr__(key, value)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.data}, default={repr(self.default_value)})"


class EnumMapping(Mapping):
    def __init__(
        self,
        values: dict,
        enum: Type[Enum],
        default_value: Any = Mapping.empty_value,
    ):

        self.enum = enum
        self.valid_keys = list(enum)
        super().__init__(
            values,
            valid_keys=self.valid_keys,
            default_value=default_value,
            read_only=True,
        )

    def key_in_valid_keys(self, key) -> bool:
        try:
            self.enum(key)
        except (KeyError, ValueError):
            return False
        else:
            return True

    def __getitem__(self, key):
        if not self.key_in_valid_keys(key):
            raise KeyError(key)

        if not isinstance(key, self.enum):
            key = self.enum(key)

        return super().__getitem__(key)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.data}, default={repr(self.default_value)})"


class RequiredKeysDict(UserDict):
    REQUIRED_KEYS: set

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validate_required_args()

    def _get_expected_kwargs(self) -> set:
        return self.REQUIRED_KEYS

    def _get_existing_kwargs(self) -> set:
        return set(self.data.keys())

    def validate_required_args(self):
        existing = self._get_existing_kwargs()
        expected = self._get_expected_kwargs()
        non_present_kwargs = expected.difference(existing)
        if len(non_present_kwargs) > 0:
            raise MissingKeys(keys=non_present_kwargs)
