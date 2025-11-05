from pydantic import ValidationInfo


def validate_identifier(value: str) -> str:
    _type, _uuid = value.split("--")
    if not _type and not _uuid:
        raise ValueError("Invalid identifier format.")
    return value


def validate_bin_field(value: str, info: ValidationInfo) -> str:
    if info.field_name and not info.field_name.endswith("_bin"):
        raise ValueError("The property name MUST end with '_bin'.")
    return value


def validate_hex_field(value: str, info: ValidationInfo) -> str:
    if info.field_name and not info.field_name.endswith("_hex"):
        raise ValueError("The property name MUST end with '_hex'.")
    return value
