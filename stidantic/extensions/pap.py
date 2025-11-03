from enum import Enum
from typing import Literal
from datetime import datetime, timezone

from stidantic.extension import ExtensionDefinition
from stidantic.types import (
    Extension,
    ExtensionType,
    Identifier,
)
from stidantic.marking import MarkingDefinition


STIX_PAP_EXT_CREATION_DATE = datetime(2022, 11, 28, 00, 00, 00, 00, tzinfo=timezone.utc)
CISA = Identifier("identity--b3bca3c2-1f3d-4b54-b44f-dac42c3a8f01")

PAPExtensionDefinition = ExtensionDefinition(
    id=Identifier(
        "extension-definition--f8d78575-edfd-406e-8e84-6162a8450f5b",
    ),
    name="pap",
    version="1.0.0",
    created=STIX_PAP_EXT_CREATION_DATE,
    modified=STIX_PAP_EXT_CREATION_DATE,
    created_by_ref=CISA,
    json_schema="https://github.com/oasis-open/cti-stix-common-objects/blob/main/extension-definition-specifications/pap-marking-definition-f8d/extension-definition--f8d78575-edfd-406e-8e84-6162a8450f5b.json",
    extension_types=[ExtensionType.property_extension],
)


class PAPExtension(Extension):
    extension_type: ExtensionType | None = ExtensionType.property_extension
    pap: Literal["white", "clear", "green", "red", "amber"]


class PAP(Enum):
    white = MarkingDefinition(
        id=Identifier("marking-definition--a3bea94c-b469-41dc-9cfe-d6e7daba7730"),
        name="PAP:WHITE",
        created=datetime(2022, 10, 1, 00, 00, 00, 00, tzinfo=timezone.utc),
        extensions={PAPExtensionDefinition.id: PAPExtension(pap="white")},
    )
    clear = MarkingDefinition(
        id=Identifier("marking-definition--ad15a0cd-55b6-4588-a14c-a66105329b92"),
        name="PAP:CLEAR",
        created=datetime(2022, 10, 1, 00, 00, 00, 00, tzinfo=timezone.utc),
        extensions={PAPExtensionDefinition.id: PAPExtension(pap="clear")},
    )
    green = MarkingDefinition(
        id=Identifier("marking-definition--c43594d1-4b11-4c59-93ab-1c9b14d53ce9"),
        name="PAP:GREEN",
        created=datetime(2022, 10, 9, 00, 00, 00, 00, tzinfo=timezone.utc),
        extensions={PAPExtensionDefinition.id: PAPExtension(pap="green")},
    )
    red = MarkingDefinition(
        id=Identifier("marking-definition--740d36e5-7714-4c30-961a-3ae632ceee0e"),
        name="PAP:RED",
        created=datetime(2022, 10, 6, 00, 00, 00, 00, tzinfo=timezone.utc),
        extensions={PAPExtensionDefinition.id: PAPExtension(pap="red")},
    )
    amber = MarkingDefinition(
        id=Identifier("marking-definition--60f8932b-e51e-4458-b265-a2e8be9a80ab"),
        name="PAP:AMBER",
        created=datetime(2022, 10, 2, 00, 00, 00, 00, tzinfo=timezone.utc),
        extensions={PAPExtensionDefinition.id: PAPExtension(pap="amber")},
    )
