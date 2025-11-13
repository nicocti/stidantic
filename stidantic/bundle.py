from typing import Annotated, Type, get_args  # pyright: ignore[reportDeprecated] # noqa: UP035

from pydantic import Field

from stidantic.extension import ExtensionDefinition
from stidantic.language import LanguageContent
from stidantic.marking import MarkingDefinition
from stidantic.sco import SCOs
from stidantic.sdo import SDOs
from stidantic.sro import SROs
from stidantic.types import ExtensionType, Identifier, StixCommon, StixCore, StixDomain, StixObservable


# 8. Stix Bundle
class StixBundle(StixCore):
    id: Identifier
    type: str = "bundle"
    objects: list[
        Annotated[
            (SROs | SDOs | SCOs | MarkingDefinition | LanguageContent | ExtensionDefinition),
            Field(discriminator="type"),
        ]
        | StixCommon
    ]

    @classmethod
    def register_new_object(
        cls,
        definition: ExtensionDefinition,  # ExtensionDefinition pyright: ignore[reportUnusedParameter]
        extension: Type[StixDomain | StixObservable],  # pyright: ignore[reportDeprecated]  # noqa: UP006
    ) -> None:
        if not (
            set(definition.extension_types)
            & {
                ExtensionType.new_sco.value,
                ExtensionType.new_sdo.value,
                ExtensionType.new_sro.value,
            }
        ):
            raise ValueError(
                "New object extension must contain new_sdo, new_sro or new_sco in the extension_types property"
            )
        annotation = cls.model_fields["objects"].annotation
        union, *_annotations = get_args(get_args(get_args(annotation)[0])[0])  # pyright: ignore[reportAny]
        cls.model_fields["objects"].annotation = list[
            Annotated[
                union | extension,
                Field(discriminator="type"),
            ]
            | StixCommon
        ]
        cls.__stix_extensions__[definition.id] = definition
        cls.model_rebuild(force=True)  # pyright: ignore[reportUnusedCallResult]
