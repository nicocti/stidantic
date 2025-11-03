"""Common reusable validators for STIX objects to improve code reusability and performance."""

from typing import Any, Self
from datetime import datetime
from pydantic import model_validator


def create_first_last_seen_validator(
    first_field: str = "first_seen",
    last_field: str = "last_seen"
):
    """
    Create a validator that ensures last_seen is after or equal to first_seen.
    
    This factory function creates a reusable validator to avoid code duplication
    across multiple STIX object classes.
    
    Args:
        first_field: Name of the first timestamp field (default: "first_seen")
        last_field: Name of the last timestamp field (default: "last_seen")
    
    Returns:
        A model_validator function that can be used as a class method
    """
    @model_validator(mode="after")
    def validate_last_after_first(self: Self) -> Self:
        """
        Validates that last timestamp is greater than or equal to first timestamp.
        """
        first_value = getattr(self, first_field, None)
        last_value = getattr(self, last_field, None)
        
        if first_value and last_value and first_value > last_value:
            raise ValueError(
                f"The {last_field} property MUST be greater than or equal to the timestamp in the {first_field} property"
            )
        return self
    
    return validate_last_after_first


def create_modified_after_created_validator(
    created_field: str = "created",
    modified_field: str = "modified"
):
    """
    Create a validator that ensures modified is after or equal to created.
    
    This factory function creates a reusable validator to avoid code duplication
    across multiple STIX object classes.
    
    Args:
        created_field: Name of the creation timestamp field (default: "created")
        modified_field: Name of the modification timestamp field (default: "modified")
    
    Returns:
        A model_validator function that can be used as a class method
    """
    @model_validator(mode="after")
    def validate_modified_after_created(self: Self) -> Self:
        """
        Validates that modified property is later than or equal to created property.
        """
        created_value = getattr(self, created_field, None)
        modified_value = getattr(self, modified_field, None)
        
        if created_value and modified_value and created_value > modified_value:
            raise ValueError(
                f"The {modified_field} property MUST be later than or equal to the value of the {created_field} property."
            )
        return self
    
    return validate_modified_after_created


def create_at_least_one_property_validator(exclude_fields: set[str] | None = None):
    """
    Create a validator that ensures at least one property is present.
    
    This factory function creates a reusable validator to avoid code duplication
    across multiple STIX object classes that require at least one property to be set.
    
    Args:
        exclude_fields: Set of field names to exclude from the check (default: {"type"})
    
    Returns:
        A model_validator function that can be used as a class method
    """
    if exclude_fields is None:
        exclude_fields = {"type"}
    
    @model_validator(mode="before")
    @classmethod
    def at_least_one(cls, data: Any) -> Any:
        """
        Validates that at least one property (other than excluded fields) is present.
        """
        if isinstance(data, dict):
            for key, value in data.items():
                if key not in exclude_fields and value is not None:
                    return data
            raise ValueError("At least one property must be present")
        raise TypeError("Input data must be a dictionary")
    
    return at_least_one
