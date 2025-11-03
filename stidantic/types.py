from enum import Enum
from re import compile
from datetime import datetime
from typing import Annotated, Literal, Any, Self, Type, get_args  # pyright: ignore[reportDeprecated]
from annotated_types import Ge, Le
from typing_extensions import TypedDict

from pydantic.functional_validators import AfterValidator, model_validator
from pydantic.networks import AnyUrl, UrlConstraints
from pydantic.types import Base64Bytes, StringConstraints
from pydantic_core import CoreSchema, core_schema
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    GetCoreSchemaHandler,
    SerializeAsAny,
)

from stidantic.validators import (
    validate_bin_field,
    validate_hex_field,
)


# Common constraints on Stix dictionnary keys.
StixKeyPattern = compile(r"^[a-zA-Z0-9\-\_]+$")
StixKeyConstraint = StringConstraints(max_length=250, pattern=StixKeyPattern)
StixKey = Annotated[str, StixKeyConstraint]

# Common constraints on Stix type names.
StixTypePattern = compile(r"^[a-zA-Z0-9\-]+$")
StixTypeConstraint = StringConstraints(pattern=StixTypePattern)
StixType = Annotated[str, StixTypeConstraint]

# Common constraints on Stix property names.
StixPropPattern = compile(r"^[a-zA-Z0-9\_]+$")
StixPropConstraint = StringConstraints(
    min_length=3, max_length=250, pattern=StixPropPattern
)
StixProp = Annotated[str, StixPropConstraint]

# 2.1 Binary
# The binary data type represents a sequence of bytes. In order to allow pattern matching on custom objects,
# for all properties that use the binary type, the property name MUST end with '_bin'.
type StixBinary = Annotated[Base64Bytes, AfterValidator(validate_bin_field)]

# 2.8 Hexadecimal
# The hex data type encodes an array of octets (8-bit bytes) as hexadecimal. The string MUST consist of an even number
# of hexadecimal characters, which are the digits '0' through '9' and the lower-case letters 'a' through 'f'. In order
# to allow pattern matching on custom objects, for all properties that use the hex type,
# the property name MUST end with '_hex'.
type StixHex = Annotated[str, AfterValidator(validate_hex_field)]

# 2.3 Dictionnary
# Dictionary keys MUST be unique in each dictionary, MUST be in ASCII, and are limited to the characters
# a-z (lowercase ASCII), A-Z (uppercase ASCII), numerals 0-9, hyphen (-), and underscore (_).
# Dictionary keys MUST be no longer than 250 ASCII characters in length and SHOULD be lowercase.
type StixDict = dict[
    StixKey,
    Any,  # pyright: ignore[reportExplicitAny]
]


# A URL reference to an external resource [RFC3986].
type StixUrl = Annotated[AnyUrl, UrlConstraints(preserve_empty_path=True)]


# 2.9 Identifier
class Identifier(str):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,  # pyright: ignore[reportExplicitAny, reportAny]
        handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(str))

    def get_type(self: str) -> str:
        return self.split("--", maxsplit=1)[0]


class StixCore(BaseModel):
    model_config = ConfigDict(  # pyright: ignore[reportUnannotatedClassAttribute]
        use_enum_values=True,
        validate_by_alias=True,
        validate_by_name=True,
        frozen=True,
        extra="allow",
    )


# 2.7 Hashes
class Hashes(StixCore, extra="allow"):
    """
    The Hashes type represents one or more cryptographic hashes, as a special set of key/value pairs.
    Accordingly, the name of each hashing algorithm MUST be specified as a key in the dictionary
    and MUST identify the name of the hashing algorithm used to generate the corresponding value.
    This name SHOULD come from one of the values defined in the hash-algorithm-ov open vocabulary.

    To enhance compatibility, the SHA-256 hash SHOULD be used whenever possible.
    """

    # Specifies the MD5 message digest algorithm. The corresponding hash string for this
    # value MUST be a valid MD5 message digest as defined in [RFC1321].
    md5: Annotated[str | None, Field(serialization_alias="MD5")] = None
    # Specifies the SHA-1 (secure-hash algorithm 1) cryptographic hash function.
    # The corresponding hash string for this value MUST be a valid SHA-1 message digest as defined in [RFC3174].
    sha1: Annotated[str | None, Field(serialization_alias="SHA-1")] = None
    # Specifies the SHA-256 cryptographic hash function (part of the SHA2 family).
    # The corresponding hash string for this value MUST be a valid SHA-256 message digest as defined in [RFC6234].
    sha256: Annotated[str | None, Field(serialization_alias="SHA-256")] = None
    # Specifies the SHA-512 cryptographic hash function (part of the SHA2 family).
    # The corresponding hash string for this value MUST be a valid SHA-512 message digest as defined in [RFC6234].
    sha512: Annotated[str | None, Field(serialization_alias="SHA-512")] = None
    # Specifies the SHA3-256 cryptographic hash function. The corresponding hash string
    # for this value MUST be a valid SHA3-256 message digest as defined in [FIPS202].
    sha3_256: Annotated[str | None, Field(serialization_alias="SHA3-256")] = None
    # Specifies the SHA3-512 cryptographic hash function. The corresponding hash string
    # for this value MUST be a valid SHA3-512 message digest as defined in [FIPS202].
    sha3_512: Annotated[str | None, Field(serialization_alias="SHA3-512")] = None
    # Specifies the ssdeep fuzzy hashing algorithm. The corresponding hash string for this
    # value MUST be a valid piecewise hash as defined in the [SSDEEP] specification.
    ssdeep: Annotated[str | None, Field(serialization_alias="SSDEEP")] = None
    # Specifies the TLSH fuzzy hashing algorithm. The corresponding hash string for this
    # value MUST be a valid 35 byte long hash as defined in the [TLSH] specification.
    tlsh: Annotated[str | None, Field(serialization_alias="TLSH")] = None

    @model_validator(mode="after")
    def lang_or_marking_ref(self) -> "Hashes":
        """
        Dictionary keys MUST be unique in each hashes property, MUST be in ASCII, and are limited to the
        characters a-z (lowercase ASCII), A-Z (uppercase ASCII), numerals 0-9, hyphen (-), and underscore (_).
        Dictionary keys MUST have a minimum length of 3 ASCII characters
        and MUST be no longer than 250 ASCII characters in length.
        The value MUST be a string in the appropriate format defined by the hash type indicated in the dictionary key.
        """
        if self.__pydantic_extra__ and any(
            not (len(key) > 250 or len(key) < 3 or StixKeyPattern.match(key))
            for key in self.__pydantic_extra__.keys()
        ):
            raise ValueError("Invalid extra hash key.")
        return self


# 2.5 External Reference
class ExternalReference(StixCore):
    """
    External references are used to describe pointers to information represented outside of STIX.
    For example, a Malware object could use an external reference to indicate an ID for that malware
    in an external database or a report could use references to represent source material.
    """

    # The name of the source that the external-reference is defined within (system, registry, organization, etc.).
    source_name: str
    # A human readable description.
    description: str | None = None
    # A URL reference to an external resource [RFC3986].
    url: StixUrl | None = None
    # Specifies a dictionary of hashes for the contents of the url. This SHOULD be provided when the url property is
    # present. Dictionary keys MUST come from one of the entries listed in the hash-algorithm-ov open vocabulary.
    # As stated in Section 2.7, to ensure interoperability, a SHA-256 hash SHOULD be included whenever possible.
    hashes: Hashes | None = None
    # An identifier for the external reference content.
    external_id: str | None = None

    @model_validator(mode="before")
    def at_least_one(cls, values: dict[str, str]) -> dict[str, str]:
        """
        In addition to the source_name property, at least one of the description, url,
        or external_id properties MUST be present.
        """
        for value in values.values():
            if value:
                return values
        raise ValueError("Missing at least one hash value.")


# 2.11 Kill Chain Phase
class KillChainPhase(StixCore):
    """
    The kill-chain-phase represents a phase in a kill chain, which describes the
    various phases an attacker may undertake in order to achieve their objectives.
    """

    # The name of the kill chain. The value of this property SHOULD be all lowercase
    # and SHOULD use hyphens instead of spaces or underscores as word separators.
    kill_chain_name: str
    # The name of the phase in the kill chain. The value of this property SHOULD be all
    # lowercase and SHOULD use hyphens instead of spaces or underscores as word separators.
    phase_name: str


# 7.2.3 Granular Markings
class GranularMarking(StixCore):
    """
    The granular-marking type defines how the list of marking-definition objects referenced by
    the marking_refs property to apply to a set of content identified by
    the list of selectors in the selectors property.
    """

    # The lang property identifies the language of the text identified by this marking. The value of the lang property,
    # if present, MUST be an [RFC5646] language code. If the marking_ref property is not present, this property MUST
    # be present. If the marking_ref property is present, this property MUST NOT be present.
    lang: str | None = None
    # The marking_ref property specifies the ID of the marking-definition object that describes the marking.
    # If the lang property is not present, this property MUST be present. If the lang property is present,
    # this property MUST NOT be present.
    marking_ref: Identifier | None = None
    # The selectors property specifies a list of selectors for content contained within the STIX Object in which this
    # property appears. Selectors MUST conform to the syntax defined below. The marking-definition referenced in
    # the marking_ref property is applied to the content selected by the selectors in this list. The [RFC5646] language
    # code specified by the lang property is applied to the content selected by the selectors in this list.
    selectors: list[str] | None = None
    # Selector Syntax:
    # Selectors contained in the selectors list are strings that consist of multiple components that MUST be separated
    # by the . character. Each component MUST be one of:
    #    ●      A property name or dictionary key, e.g., description, or;
    #    ●      A zero-based list index, specified as a non-negative integer in square brackets, e.g., [4]
    # Selectors denote path traversals: the root of each selector is the STIX Object
    # that the granular_markings property appears in.
    # Starting from that root, for each component in the selector, properties and list items are traversed.
    # When the complete list has been traversed, the value of the content is considered selected.
    # Selectors MUST refer to properties or list items that are actually present on the marked object.

    @model_validator(mode="after")
    def lang_or_marking_ref(self) -> "GranularMarking":
        if self.lang and self.marking_ref:
            raise ValueError(
                "Both lang and marking_ref properties MUST NOT be present."
            )
        if not self.lang and not self.marking_ref:
            raise ValueError("Either lang or marking_ref property MUST be present.")
        return self


# 10.5 Extension Types Enumeration
class ExtensionType(Enum):
    new_sdo = "new-sdo"
    new_sco = "new-sco"
    new_sro = "new-sro"
    property_extension = "property-extension"
    toplevel_property_extension = "toplevel-property-extension"


class Extension(StixCore):
    extension_type: ExtensionType | None = None


class ExtensionsDict(TypedDict, total=False, extra_items=SerializeAsAny[Extension]): ...  # noqa: E701


# 3.2 Common Properties
class StixCommon(StixCore):
    """
    This section defines the common properties that MAY exist on a STIX Objects. While some STIX Objects use all
    of these common properties, not all object types do.
    Each type of STIX Object defines which common properties are required, which are optional,
    and which are not in use.
    """

    # All STIX Objects and the STIX Bundle Object have an id property that uniquely identifies each instance
    # of the object.
    # This id MUST meet the requirements of the identifier type (see section 2.9).
    # For objects that support versioning, all objects with the same id are considered different versions
    # of the same object and the version of the object is identified by its modified property.
    id: Identifier
    # The type property identifies the type of STIX Object.
    type: str
    # The value of this property MUST be 2.1 for STIX Objects defined according to this specification.
    spec_version: Literal["2.1"] = "2.1"
    # The revoked property is only used by STIX Objects that support versioning and indicates whether the object
    # has been revoked.
    revoked: bool | None = None
    # The labels property specifies a set of terms used to describe this object.
    # Where an object has a specific property defined in the specification for characterizing
    # subtypes of that object, the labels property MUST NOT be used for that purpose.
    labels: list[str] | None = None
    # The confidence property identifies the confidence that the creator has in the correctness of their data.
    # The confidence value MUST be a number in the range of 0-100.
    confidence: Annotated[int, Ge(0), Le(100)] | None = None
    # The lang property identifies the language of the text content in this object.
    # When present, it MUST be a language code conformant to [RFC5646].
    # RFC5646 does not enforce ISO 639-1 alpha-2 or ISO 639-3 alpha-3 formats.
    lang: str | None = None
    # The external_references property specifies a list of external references which refers to non-STIX information.
    external_references: list[ExternalReference] | None = None
    # The object_marking_refs property specifies a list of id properties of marking-definition objects that apply
    # to this object.
    object_marking_refs: list[Identifier] | None = None
    # The granular_markings property specifies a list of granular markings applied to this object.
    granular_markings: list[GranularMarking] | None = None
    # Specifies any extensions of the object, as a dictionary.
    # Dictionary keys SHOULD be the id of a STIX Extension object or the name of a predefined object extension found
    # in this specification, depending on the type of extension being used.
    # The corresponding dictionary values MUST contain the contents of the extension instance.
    # Each extension dictionary MAY contain the property extension_type.
    # The value of this property MUST come from the extension-type-enum enumeration.
    # If the extension_type property is not present, then this is a predefined extension which
    # does not use the extension facility described in section 7.3.
    # When this extension facility is used the extension_type property MUST be present.
    extensions: ExtensionsDict | dict[str, Extension] | None = None

    @classmethod
    def register_new_extension(
        cls,
        definition: "StixCommon",  # pyright: ignore[reportUnusedParameter]
        extension: Type[Extension],  # pyright: ignore[reportUnusedParameter, reportDeprecated]
    ):
        """
        Dynamically update the extensions property so that new classes get deserialized based on the extension key.
        """
        annotations = get_args(cls.model_fields["extensions"].annotation)[0]  # pyright: ignore[reportAny, reportUnusedVariable]
        CustomExtensionsDict = TypedDict(
            "CustomExtensionsDict",
            {
                definition.id: extension,  # pyright: ignore[reportGeneralTypeIssues]
                **annotations.__annotations__,  # pyright: ignore[reportGeneralTypeIssues]
            },
            total=False,
            extra_items=SerializeAsAny[Extension],
        )
        cls.model_fields["extensions"].annotation = CustomExtensionsDict | None  # pyright: ignore[reportAttributeAccessIssue]
        cls.model_rebuild(force=True)  # pyright: ignore[reportUnusedCallResult]


class StixDomain(StixCommon):
    # The created_by_ref property specifies the id property of the identity object that describes the entity that
    # created this object.
    created_by_ref: Identifier | None = None
    # The created property represents the time at which the object was originally created.
    # The created property MUST NOT be changed when creating a new version of the object.
    created: datetime
    # The modified property is only used by STIX Objects that support versioning and represents
    # the time that this particular version of the object was last modified.
    # Object creators MUST set the modified property when creating a new
    # version of an object if the created property was set.
    modified: datetime

    @model_validator(mode="after")
    def validate_modified_after_created(self) -> Self:
        """
        If the created property is defined, then the value of the modified property for a given object version
        MUST be later than or equal to the value of the created property.
        """
        if self.created > self.modified:
            raise ValueError(
                "The modified property MUST be later than or equal to the value of the created property."
            )
        return self


class StixObservable(StixCommon):
    # This property defines whether or not the data contained within the object has been defanged.
    defanged: bool | None = None


class StixRelationship(StixCommon):
    relationship_type: str
    # The created property represents the time at which the object was originally created.
    # The created property MUST NOT be changed when creating a new version of the object.
    created: datetime
    # The modified property is only used by STIX Objects that support versioning and represents
    # the time that this particular version of the object was last modified.
    # Object creators MUST set the modified property when creating a new
    # version of an object if the created property was set.
    modified: datetime
    # The created_by_ref property specifies the id property of the identity object that describes the entity that
    # created this object.
    created_by_ref: Identifier | None = None

    @model_validator(mode="after")
    def validate_modified_after_created(self) -> Self:
        """
        If the created property is defined, then the value of the modified property for a given object version
        MUST be later than or equal to the value of the created property.
        """
        if self.created > self.modified:
            raise ValueError(
                "The modified property MUST be later than or equal to the value of the created property."
            )
        return self


class StixMeta(StixCommon):
    type: str
    # The created property represents the time at which the object was originally created.
    # The created property MUST NOT be changed when creating a new version of the object.
    created: datetime


class StixLanguage(StixMeta):
    # The created_by_ref property specifies the id property of the identity object that describes the entity that
    # created this object.
    created_by_ref: Identifier | None = None
    # The modified property is only used by STIX Objects that support versioning and represents
    # the time that this particular version of the object was last modified.
    # Object creators MUST set the modified property when creating a new
    # version of an object if the created property was set.
    modified: datetime

    @model_validator(mode="after")
    def validate_modified_after_created(self) -> Self:
        """
        If the created property is defined, then the value of the modified property for a given object version
        MUST be later than or equal to the value of the created property.
        """
        if self.created > self.modified:
            raise ValueError(
                "The modified property MUST be later than or equal to the value of the created property."
            )
        return self


class StixMarking(StixMeta):
    # The created_by_ref property specifies the id property of the identity object that describes the entity that
    # created this object.
    created_by_ref: Identifier | None = None


class StixExtension(StixMeta):
    # The created_by_ref property specifies the id property of the identity object that describes the entity that
    # created this object.
    created_by_ref: Identifier
    # The modified property is only used by STIX Objects that support versioning and represents
    # the time that this particular version of the object was last modified.
    # Object creators MUST set the modified property when creating a new
    # version of an object if the created property was set.
    modified: datetime

    @model_validator(mode="after")
    def validate_modified_after_created(self) -> Self:
        """
        If the created property is defined, then the value of the modified property for a given object version
        MUST be later than or equal to the value of the created property.
        """
        if self.created > self.modified:
            raise ValueError(
                "The modified property MUST be later than or equal to the value of the created property."
            )
        return self
