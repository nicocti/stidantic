from typing import Literal, Self
from typing_extensions import Annotated
from pydantic.functional_validators import model_validator
from pydantic import Field
from stidantic.types import StixObservable, StixBinary, StixUrl, Hashes
from stidantic.vocab import EncryptionAlgorithm


# 6.1 Artifact Object
class Artifact(StixObservable):
    """
    The Artifact Object permits capturing an array of bytes (8-bits),
    as a base64-encoded string string, or linking to a file-like payload.
    """

    type: Literal["artifact"] = "artifact"  # pyright: ignore[reportIncompatibleVariableOverride]
    mime_type: str | None = None
    payload_bin: StixBinary | None = None
    url: StixUrl | None = None
    hashes: Hashes | None = None
    encryption_algorithm: EncryptionAlgorithm | None = None
    decryption_key: str | None = None

    @model_validator(mode="after")
    def one_of(self) -> Self:
        """
        One of payload_bin or url MUST be provided.
        """
        if self.payload_bin or self.hashes:
            return self
        raise ValueError("Missing at least hashes or payload_bin property.")

    @model_validator(mode="after")
    def url_must_not_be_present_if_payload_bin_provided(self) -> Self:
        """
        URL property MUST NOT be present if payload_bin is provided.
        """
        if self.payload_bin and self.url:
            raise ValueError(
                "url property MUST NOT be present if payload_bin is provided."
            )
        return self

    @model_validator(mode="after")
    def hashes_must_be_present_if_url_provided(self) -> Self:
        """
        Hashes property MUST be present when the url property is present.
        """
        if self.url and not self.hashes:
            raise ValueError("hashes MUST be present if url is provided.")
        return self

    @model_validator(mode="after")
    def decryption_key_must_not_be_present_if_encryption_algorithm_absent(self) -> Self:
        """
        decryption_key property MUST NOT be present when the encryption_algorithm property is absent.
        """
        if not self.encryption_algorithm and self.decryption_key:
            raise ValueError(
                "decryption_key MUST NOT be present when the encryption_algorithm property is absent."
            )
        return self

    class Config:
        json_schema_extra: dict[str, list[str]] = {
            "id_contributing_properties": ["hashes", "payload_bin"]
        }


# 6.2 Autonomous System
class AutonomousSystem(StixObservable):
    """
    The AS object represents the properties of an Autonomous Systems (AS).
    """

    type: Literal["autonomous-system"] = "autonomous-system"  # pyright: ignore[reportIncompatibleVariableOverride]
    # Specifies the number assigned to the AS. Such assignments a
    # re typically performed by a Regional Internet Registry (RIR).
    number: int
    # Specifies the name of the AS.
    name: str | None = None
    # Specifies the name of the Regional Internet Registry (RIR) that assigned the number to the AS.
    rir: str | None = None

    class Config:
        json_schema_extra: dict[str, list[str]] = {
            "id_contributing_properties": ["number"]
        }


SCOs = Annotated[(Artifact | AutonomousSystem), Field(discriminator="type")]
