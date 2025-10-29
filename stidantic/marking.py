from typing import Literal, Self
from enum import Enum
from datetime import datetime, timezone

from pydantic.functional_validators import model_validator
from stidantic.types import (
    StixCore,
    StixMarking,
    Identifier,
)


# 7.2.1.3 Statement Marking
class StatementMarking(StixCore):
    """
    The Statement marking type defines the representation of a textual marking statement (e.g., copyright, terms of use,
    etc.) in a definition. The value of the definition_type property MUST be statement when using this marking type.
    Statement markings are generally not machine-readable, and this specification does not define any behavior or
    actions based on their values.

    Content may be marked with multiple statements of use. In other words, the same content can be marked both with a
    statement saying "Copyright 2019" and a statement saying, "Terms of use are ..." and both statements apply.
    """

    # A Statement (e.g., copyright, terms of use) applied to the content marked by this marking definition.
    statement: str


# 7.2.1.4 TLP Marking
class TLPMarking(StixCore):
    """
    The TLP marking type defines how you would represent a Traffic Light Protocol (TLP) marking in a definition
    property. The value of the definition_type property MUST be tlp when using this marking type.
    """

    # The TLP level [TLP] of the content marked by this marking definition, as defined in this section.
    tlp: str


# 7.2.1 Marking Definition
class MarkingDefinition(StixMarking):
    """
    The marking-definition object represents a specific marking. Data markings typically represent handling or
    sharing requirements for data and are applied in the object_marking_refs and granular_markings properties on
    STIX Objects, which reference a list of IDs for marking-definition objects.

    Two marking definition types are defined in this specification: TLP, to capture TLP markings, and Statement,
    to capture text marking statements. In addition, it is expected that the FIRST Information Exchange Policy (IEP)
    will be included in a future version once a machine-usable specification for it has been defined.

    Unlike other STIX Objects, Marking Definition objects cannot be versioned because it would allow for indirect
    changes to the markings on a STIX Object. For example, if a Statement marking is changed from "Reuse Allowed" to
    "Reuse Prohibited", all STIX Objects marked with that Statement marking would effectively have an updated marking
    without being updated themselves. Instead, a new Statement marking with the new text should be created and the
    marked objects updated to point to the new marking.
    """

    type: Literal["marking-definition"] = "marking-definition"  # pyright: ignore[reportIncompatibleVariableOverride]
    # A name used to identify the Marking Definition.
    name: str | None = None
    # The definition_type property identifies the type of Marking Definition. The value of the definition_type property
    # SHOULD be one of the types defined in the subsections below: statement or tlp (see sections 7.2.1.3 and 7.2.1.4).
    # Any new marking definitions SHOULD be specified using the extension facility described in section 7.3.
    # If the extensions property is not present, this property MUST be present.
    definition_type: str | None = None
    # The definition property contains the marking object itself (e.g., the TLP marking as defined in section 7.2.1.4,
    # the Statement marking as defined in section 7.2.1.3).
    # Any new marking definitions SHOULD be specified using the extension facility described in section 7.3.
    # If the extensions property is not present, this property MUST be present.
    definition: TLPMarking | StatementMarking | None = None

    @model_validator(mode="after")
    def definition_if_no_extensions(self) -> Self:
        if not self.extensions and (not self.definition and not self.definition_type):
            raise ValueError(
                "If the extensions property is not present, definition_type and definition properties MUST be present."
            )
        return self


STIX_ZERO_DATE = datetime(2017, 1, 20, 00, 00, 00, 00, tzinfo=timezone.utc)


class TLP(Enum):
    """
    The following standard marking definitions MUST be used to reference or represent TLP markings.
    Other instances of tlp-marking MUST NOT be used or created (the only instances of TLP marking definitions
    permitted are those defined here).
    """

    white = MarkingDefinition(
        id=Identifier("marking-definition--613f2e26-407d-48c7-9eca-b8e91df99dc9"),
        definition_type="tlp",
        definition=TLPMarking(tlp="white"),
        name="TLP:WHITE",
        created=STIX_ZERO_DATE,
    )
    green = MarkingDefinition(
        id=Identifier("marking-definition--34098fce-860f-48ae-8e50-ebd3cc5e41da"),
        definition_type="tlp",
        definition=TLPMarking(tlp="green"),
        name="TLP:GREEN",
        created=STIX_ZERO_DATE,
    )
    amber = MarkingDefinition(
        id=Identifier("marking-definition--f88d31f6-486f-44da-b317-01333bde0b82"),
        definition_type="tlp",
        definition=TLPMarking(tlp="amber"),
        name="TLP:AMBER",
        created=STIX_ZERO_DATE,
    )
    red = MarkingDefinition(
        id=Identifier("marking-definition--5e57c739-391a-4eb3-b6be-7d15ca92d5ed"),
        definition_type="tlp",
        definition=TLPMarking(tlp="red"),
        name="TLP:RED",
        created=STIX_ZERO_DATE,
    )
