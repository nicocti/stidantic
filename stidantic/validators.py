from collections.abc import Callable

from pydantic import ValidationInfo


def validate_identifier(value: str, types: tuple[str, ...]) -> str:
    t = value.split("--")[0]
    if t not in types:
        raise ValueError(f"{value} is not one of {types}")
    return value


def identifier_of_type(*args: str) -> Callable[..., str]:
    """
    Validates that an identifier is of a certain type or types.
    """

    def validator(value: str) -> str:
        return validate_identifier(value, args)

    return validator


def validate_bin_field(value: str, info: ValidationInfo) -> str:
    if info.field_name and not info.field_name.endswith("_bin"):
        raise ValueError("The property name MUST end with '_bin'.")
    return value


def validate_hex_field(value: str, info: ValidationInfo) -> str:
    if info.field_name and not info.field_name.endswith("_hex"):
        raise ValueError("The property name MUST end with '_hex'.")
    return value
