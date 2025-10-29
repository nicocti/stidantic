from typing import Annotated
from pydantic import Field
from stidantic.types import StixCore, Identifier, StixCommon
from stidantic.sdo import SDOs
from stidantic.sco import SCOs
from stidantic.sro import SROs
from stidantic.language import LanguageContent
from stidantic.marking import MarkingDefinition
from stidantic.extension import ExtensionDefinition


# 8. Stix Bundle
class StixBundle(StixCore):
    id: Identifier
    type: str = "bundle"
    objects: list[
        Annotated[
            (
                SROs
                | SDOs
                | SCOs
                | MarkingDefinition
                | LanguageContent
                | ExtensionDefinition
            ),
            Field(discriminator="type"),
        ]
        | StixCommon
    ]
