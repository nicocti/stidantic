import ipaddress
from datetime import datetime
from annotated_types import Ge, Le
from typing_extensions import Annotated, TypedDict
from typing import Any, Literal, Self

from pydantic.functional_serializers import SerializeAsAny
from pydantic.functional_validators import model_validator
from pydantic.types import JsonValue
from pydantic import Field

from stidantic.types import (
    Extension,
    StixCore,
    StixObservable,
    StixBinary,
    StixUrl,
    Hashes,
    Identifier,
)
from stidantic.vocab import (
    EncryptionAlgorithm,
    NetworkSocketAddressFamily,
    NetworkSocketType,
    WindowsIntegrityLevel,
    WindowsServiceStartType,
    WindowsServiceStatus,
    WindowsServiceType,
    WindowsRegistryDatatype,
)
from stidantic.common_validators import create_at_least_one_property_validator


# 6.1 Artifact Object
class Artifact(StixObservable):
    """
    The Artifact Object permits capturing an array of bytes (8-bits),
    as a base64-encoded string string, or linking to a file-like payload.

    It is incumbent on sharing communities to ensure that the URL is accessible for downstream consumers.
    """

    type: Literal["artifact"] = "artifact"  # pyright: ignore[reportIncompatibleVariableOverride]
    # Whenever feasible, this value SHOULD be one of the values defined in the Template column in the IANA media type
    # registry [Media Types]. Maintaining a comprehensive universal catalog of all extant file types is obviously
    # not possible. When specifying a MIME Type not included in the IANA registry, implementers should use their best
    # judgement so as to facilitate interoperability.
    mime_type: str | None = None
    # Specifies the binary data contained in the artifact as a base64-encoded string.
    payload_bin: StixBinary | None = None
    # The value of this property MUST be a valid URL that resolves to the unencoded content.
    url: StixUrl | None = None
    # Specifies a dictionary of hashes for the contents of the url or the payload_bin.
    hashes: Hashes | None = None
    # If the artifact is encrypted, specifies the type of encryption algorithm the binary data
    # (either via payload_bin or url) is encoded in.
    # If both mime_type and encryption_algorithm are included, this signifies that the artifact represents an
    # encrypted archive.
    encryption_algorithm: EncryptionAlgorithm | None = None
    # Specifies the decryption key for the encrypted binary data (either via payload_bin or url). For example,
    # this may be useful in cases of sharing malware samples, which are often encoded in an encrypted archive.
    decryption_key: str | None = None

    @model_validator(mode="after")
    def at_least_one_of(self) -> Self:
        """
        One of payload_bin or url MUST be provided.
        """
        if self.payload_bin or self.hashes:
            return self
        raise ValueError("Missing at least hashes or payload_bin property.")

    @model_validator(mode="after")
    def url_must_not_be_present_if_payload_bin_provided(self) -> Self:
        """
        The url property MUST NOT be present if payload_bin is provided.
        """
        if self.payload_bin and self.url:
            raise ValueError(
                "The url property MUST NOT be present if payload_bin is provided"
            )
        return self

    @model_validator(mode="after")
    def hashes_must_be_present_if_url_provided(self) -> Self:
        """
        The hashes property MUST be present when the url property is present.
        """
        if self.url and not self.hashes:
            raise ValueError("The hashes property MUST be present if url is provided")
        return self

    @model_validator(mode="after")
    def decryption_key_must_not_be_present_if_encryption_algorithm_absent(self) -> Self:
        """
        The decryption_key property MUST NOT be present when the encryption_algorithm property is absent.
        """
        if not self.encryption_algorithm and self.decryption_key:
            raise ValueError(
                "The decryption_key MUST NOT be present when the encryption_algorithm property is absent"
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


# 6.3 Directory Object
class Directory(StixObservable):
    """
    The Directory object represents the properties common to a file system directory.
    """

    type: Literal["directory"] = "directory"  # pyright: ignore[reportIncompatibleVariableOverride]
    # Specifies the path, as originally observed, to the directory on the file system.
    path: str
    # Specifies the observed encoding for the path. The value MUST be specified if the path is stored in a
    # non-Unicode encoding. This value MUST be specified using the corresponding name from the 2013-12-20
    # revision of the IANA character set registry [Character Sets]. If the preferred MIME name for a character
    # set is defined, this value MUST be used; if it is not defined, then the Name value from the registry
    # MUST be used instead.
    path_enc: str | None = None
    # Specifies the date/time the directory was created.
    ctime: datetime | None = None
    # Specifies the date/time the directory was last written to/modified.
    mtime: datetime | None = None
    # Specifies the date/time the directory was last accessed.
    atime: datetime | None = None
    # Specifies a list of references to other File and/or Directory objects contained within the directory.
    # The objects referenced in this list MUST be of type file or directory.
    contains_refs: list[Identifier] | None = None

    class Config:
        json_schema_extra: dict[str, list[str]] = {
            "id_contributing_properties": ["path"]
        }


# 6.4 Domain Name Object
class DomainName(StixObservable):
    """
    The Domain Name object represents the properties of a network domain name.
    """

    # NOTE: As for the validation of the value field, a complex regular expression could be used to validate the
    # domain name structure. However, fully compliant regex for domain names is notoriously difficult and prone to
    # errors, especially with internationalized domain names (IDNs). A more robust solution would be to use a dedicated
    # library for domain name parsing and validation.

    type: Literal["domain-name"] = "domain-name"  # pyright: ignore[reportIncompatibleVariableOverride]
    # Specifies the value of the domain name. The value of this property MUST conform to [RFC1034], and each
    # domain and sub-domain contained within the domain name MUST conform to [RFC5890].
    value: str
    # Specifies a list of references to one or more IP addresses or domain names that the domain name resolves to.
    # The objects referenced in this list MUST be of type ipv4-addr or ipv6-addr or domain-name
    # (for cases such as CNAME records).
    resolves_to_refs: list[Identifier] | None = None

    class Config:
        json_schema_extra: dict[str, list[str]] = {
            "id_contributing_properties": ["value"]
        }


# 6.5 Email Address Object
class EmailAddress(StixObservable):
    """
    The Email Address object represents a single email address.
    """

    type: Literal["email-addr"] = "email-addr"  # pyright: ignore[reportIncompatibleVariableOverride]
    # Specifies the value of the email address. This MUST NOT include the display name.
    # This property corresponds to the addr-spec construction in section 3.4 of [RFC5322].
    value: str
    # Specifies a single email display name, i.e., the name that is displayed to the human user of a mail application.
    # This property corresponds to the display-name construction in section 3.4 of [RFC5322].
    display_name: str | None = None
    # Specifies the user account that the email address belongs to, as a reference to a User Account object.
    # The object referenced in this property MUST be of type user-account.
    belongs_to_ref: Identifier | None = None

    class Config:
        json_schema_extra: dict[str, list[str]] = {
            "id_contributing_properties": ["value"]
        }


# 6.6.2 Email MIME Component Type
class EmailMimeComponent(StixCore):
    """
    Specifies one component of a multi-part email body.

    There is no property to capture the value of the "Content-Transfer-Encoding" header field, since the body MUST be
    decoded before being represented in the body property.
    """

    # Specifies the contents of the MIME part if the content_type is not provided or starts with text/
    # (e.g., in the case of plain text or HTML email).
    # For inclusion in this property, the contents MUST be decoded to Unicode. Note that the charset provided in
    # content_type is for informational usage and not for decoding of this property.
    body: str | None = None
    # Specifies the contents of non-textual MIME parts, that is those whose content_type does not start with text/,
    # as a reference to an Artifact object or File object.
    # The object referenced in this property MUST be of type artifact or file.
    # For use cases where conveying the actual data contained in the MIME part is of primary importance,
    # artifact SHOULD be used. Otherwise, for use cases where conveying metadata about the file-like properties of the
    # MIME part is of primary importance, file SHOULD be used.
    body_raw_ref: Identifier | None = None
    # Specifies the value of the "Content-Type" header field of the MIME part.
    # Any additional "Content-Type" header field parameters such as charset SHOULD be included in this property.
    content_type: str | None = None
    # Specifies the value of the "Content-Disposition" header field of the MIME part.
    content_disposition: str | None = None

    @model_validator(mode="after")
    def validate_body_or_body_raw_ref(self) -> Self:
        """
        One of body OR body_raw_ref MUST be included.
        """
        if self.body is None and self.body_raw_ref is None:
            raise ValueError("One of body or body_raw_ref MUST be included")
        return self


# 6.6 Email Message Object
class EmailMessage(StixObservable):
    """
    The Email Message object represents an instance of an email message, corresponding to the internet message format
    described in [RFC5322] and related RFCs.

    Header field values that have been encoded as described in section 2 of [RFC2047] MUST be decoded before inclusion
    in Email Message object properties. For example, this is some text MUST be used instead of
    =?iso-8859-1?q?this=20is=20some=20text?=. Any characters in the encoded value which cannot be decoded into Unicode
    SHOULD be replaced with the 'REPLACEMENT CHARACTER' (U+FFFD). If it is necessary to capture the header value as
    observed, this can be achieved by referencing an Artifact object through the raw_email_ref property.
    """

    type: Literal["email-message"] = "email-message"  # pyright: ignore[reportIncompatibleVariableOverride]
    # Indicates whether the email body contains multiple MIME parts.
    is_multipart: bool
    # Specifies the date/time that the email message was sent.
    date: datetime | None = None
    # Specifies the value of the "Content-Type" header of the email message.
    content_type: str | None = None
    # Specifies the value of the "From:" header of the email message.
    # The "From:" field specifies the author of the message, that is, the mailbox(es) of the person or system
    # responsible for the writing of the message.
    from_ref: Identifier | None = None
    # Specifies the value of the "Sender" field of the email message.
    # The "Sender:" field specifies the mailbox of the agent responsible for the actual transmission of the message.
    sender_ref: Identifier | None = None
    # Specifies the mailboxes that are "To:" recipients of the email message.
    to_refs: list[Identifier] | None = None
    # Specifies the mailboxes that are "CC:" recipients of the email message.
    cc_refs: list[Identifier] | None = None
    # Specifies the mailboxes that are "BCC:" recipients of the email message.
    # As per [RFC5322], the absence of this property should not be interpreted as semantically equivalent to an absent
    # BCC header on the message being characterized.
    bcc_refs: list[Identifier] | None = None
    # Specifies the Message-ID field of the email message.
    message_id: str | None = None
    # Specifies the subject of the email message.
    subject: str | None = None
    # Specifies one or more "Received" header fields that may be included in the email headers.
    # List values MUST appear in the same order as present in the email message.
    received_lines: list[str] | None = None
    # Specifies any other header fields found in the email message, as a dictionary.
    # Each key/value pair in the dictionary represents the name/value of a single header field or names/values of a
    # header field that occurs more than once. Each dictionary key SHOULD be a case-preserved version of the header
    # field name. The corresponding value for each dictionary key MUST always be a list of type string to support when
    # a header field is repeated.
    additional_header_fields: dict[str, list[str]] | None = None
    # Specifies a string containing the email body.
    body: str | None = None
    # Specifies a list of the MIME parts that make up the email body.
    body_multipart: list[EmailMimeComponent] | None = None
    # Specifies the raw binary contents of the email message, including both the headers and body, as a reference
    # to an Artifact object. The object referenced in this property MUST be of type artifact.
    raw_email_ref: Identifier | None = None

    @model_validator(mode="after")
    def validate_body(self) -> Self:
        """
        The property body MUST NOT be used if is_multipart is true.
        The property body_multipart MUST NOT be used if is_multipart is false.
        """
        if self.is_multipart and self.body is not None:
            raise ValueError("body MUST NOT be used if is_multipart is true")
        if not self.is_multipart and self.body_multipart is not None:
            raise ValueError("body_multipart MUST NOT be used if is_multipart is false")
        return self

    class Config:
        json_schema_extra: dict[str, list[str]] = {
            "id_contributing_properties": ["from_ref", "subject", "body"]
        }


# 6.7.2 Archive File Extension
class ArchiveFileExtension(Extension):
    """
    The Archive File extension specifies a default extension for capturing properties specific to archive files.
    The key for this extension when used in the extensions dictionary MUST be archive-ext.
    Note that this predefined extension does not use the extension facility described in section 7.3.
    """

    # This property specifies the files that are contained in the archive. It MUST contain references to one or more
    # File objects. The objects referenced in this list MUST be of type file or directory.
    contains_refs: list[Identifier]
    # Specifies a comment included as part of the archive file.
    comment: str | None = None


# 6.7.3.2 Alternate Data Stream Type
class AlternateDataStream(StixCore):
    """
    The Alternate Data Stream type represents an NTFS alternate data stream.
    """

    # Specifies the name of the alternate data stream.
    name: str
    # Specifies a dictionary of hashes for the data contained in the alternate data stream.
    # Dictionary keys MUST come from the hash-algorithm-ov open vocabulary.
    hashes: Hashes | None = None
    # Specifies the size of the alternate data stream, in bytes. The value of this property MUST NOT be negative.
    size: Annotated[int, Ge(0)] | None = None


# 6.7.3 NTFS File Extension
class NTFSFileExtension(Extension):
    """
    The NTFS File extension specifies a set of properties specific to files stored on NTFS file systems.

    The key for this extension when used in the extensions dictionary MUST be ntfs-ext. Note that this predefined
    extension does not use the extension facility described in section 7.3.
    """

    # Specifies the security ID (SID) value assigned to the file.
    sid: str | None = None
    # Specifies a list of NTFS alternate data streams that exist for the file.
    alternate_data_streams: list[AlternateDataStream] | None = None

    @model_validator(mode="after")
    def at_least_one_of(self) -> Self:
        """
        An object using the NTFS File Extension MUST contain at least one property from this extension.
        """
        if self.sid is None and self.alternate_data_streams is None:
            raise ValueError("At least one property must be present")
        return self


# 6.7.4 PDF File Extension
class PDFFileExtension(Extension):
    """
    The PDF file extension specifies a default extension for capturing properties specific to PDF files.

    The key for this extension when used in the extensions dictionary MUST be pdf-ext.

    Note that this predefined extension does not use the extension facility described in section 7.3.
    """

    # Specifies the decimal version number of the string from the PDF header that specifies the version of the PDF
    # specification to which the PDF file conforms. E.g 1.4
    version: str | None = None
    # Specifies whether the PDF file has been optimized.
    is_optimized: bool | None = None
    # Specifies details of the PDF document information dictionary (DID), which includes properties like the document
    # creation date and producer, as a dictionary. Each key in the dictionary SHOULD be a case-preserved version of
    # the corresponding entry in the document information dictionary without the prepended forward slash, e.g., Title.
    # The corresponding value for the key MUST be the value specified for the document information dictionary entry,
    # as a string.
    document_info_dict: dict[str, str] | None = None
    # Specifies the first file identifier found for the PDF file.
    pdfid0: str | None = None
    # Specifies the second file identifier found for the PDF file.
    pdfid1: str | None = None

    @model_validator(mode="after")
    def at_least_one_of(self) -> Self:
        """
        An object using the PDF File Extension MUST contain at least one property from this extension.
        """
        if (
            self.version is None
            and self.is_optimized is None
            and self.document_info_dict is None
            and self.pdfid0 is None
            and self.pdfid1 is None
        ):
            raise ValueError("At least one property must be present")
        return self


# 6.7.5 Raster Image File Extension
class RasterImageFileExtension(Extension):
    """
    The Raster Image file extension specifies a default extension for capturing properties specific to raster image
    files.

    The key for this extension when used in the extensions dictionary MUST be raster-image-ext. Note that this
    predefined extension does not use the extension facility described in section 7.3.
    """

    # Specifies the height of the image in the image file, in pixels.
    image_height: int | None = None
    # Specifies the width of the image in the image file, in pixels.
    image_width: int | None = None
    # Specifies the sum of bits used for each color channel in the image file, and thus the total number of pixels
    # used for expressing the color depth of the image.
    bits_per_pixel: int | None = None
    # Specifies the set of EXIF tags found in the image file, as a dictionary. Each key/value pair in the dictionary
    # represents the name/value of a single EXIF tag. Accordingly, each dictionary key MUST be a case-preserved
    # version of the EXIF tag name, e.g., XResolution. Each dictionary value MUST be either an integer
    # (for int* EXIF datatypes) or a string (for all other EXIF datatypes).
    exif_tags: dict[str, int | str] | None = None

    @model_validator(mode="after")
    def at_least_one_of(self) -> Self:
        """
        An object using the Raster Image File Extension MUST contain at least one property from this extension.
        """
        if (
            self.image_height is None
            and self.image_width is None
            and self.bits_per_pixel is None
            and self.exif_tags is None
        ):
            raise ValueError("At least one property must be present")
        return self


# 6.7.6.3 Windows PE Section Type
class WindowsPESection(StixCore):
    """
    The Windows PE Section type specifies metadata about a PE file section.
    """

    # Specifies the name of the section.
    name: str
    # Specifies the size of the section, in bytes. The value of this property MUST NOT be negative.
    size: Annotated[int, Ge(0)] | None = None
    # Specifies the calculated entropy for the section, as calculated using the Shannon algorithm [Shannon Entropy].
    # The size of each input character is defined as a byte, resulting in a possible range of 0 through 8.
    entropy: float | None = None
    # Specifies any hashes computed over the section.
    hashes: Hashes | None = None


# 6.7.6.2 Windows PE Optional Header Type
class WindowsPEOptionalHeader(StixCore):
    """
    The Windows PE Optional Header type represents the properties of the PE optional header.
    An object using the Windows PE Optional Header Type MUST contain at least one property from this type.
    """

    # Specifies the hex value that indicates the type of the PE binary.
    magic_hex: str | None = None
    # Specifies the linker major version number.
    major_linker_version: int | None = None
    # Specifies the linker minor version number.
    minor_linker_version: int | None = None
    # Specifies the size of the code (text) section.
    # If there are multiple such sections, this refers to the sum of the sizes of each section.
    size_of_code: Annotated[int, Ge(0)] | None = None
    # Specifies the size of the initialized data section.
    # If there are multiple such sections, this refers to the sum of the sizes of each section.
    size_of_initialized_data: Annotated[int, Ge(0)] | None = None
    # Specifies the size of the uninitialized data section.
    # If there are multiple such sections, this refers to the sum of the sizes of each section.
    size_of_uninitialized_data: Annotated[int, Ge(0)] | None = None
    # Specifies the address of the entry point relative to the image base when the executable is loaded into memory.
    address_of_entry_point: int | None = None
    # Specifies the address that is relative to the image base of the beginning-of-code section when it is loaded
    # into memory.
    base_of_code: int | None = None
    # Specifies the address that is relative to the image base of the beginning-of-data section when it is loaded
    # into memory.
    base_of_data: int | None = None
    # Specifies the preferred address of the first byte of the image when loaded into memory.
    image_base: int | None = None
    # Specifies the alignment (in bytes) of PE sections when they are loaded into memory.
    section_alignment: int | None = None
    # Specifies the factor (in bytes) that is used to align the raw data of sections in the image file.
    file_alignment: int | None = None
    # Specifies the major version number of the required operating system.
    major_os_version: int | None = None
    # Specifies the minor version number of the required operating system.
    minor_os_version: int | None = None
    # Specifies the major version number of the image.
    major_image_version: int | None = None
    # Specifies the minor version number of the image.
    minor_image_version: int | None = None
    # Specifies the major version number of the subsystem.
    major_subsystem_version: int | None = None
    # Specifies the minor version number of the subsystem.
    minor_subsystem_version: int | None = None
    # Specifies the reserved win32 version value.
    win32_version_value_hex: str | None = None
    # Specifies the size of the image in bytes, including all headers, as the image is loaded in memory.
    size_of_image: Annotated[int, Ge(0)] | None = None
    # Specifies the combined size of the MS-DOS, PE header, and section headers, rounded up to a multiple of the
    # value specified in the file_alignment header.
    size_of_headers: Annotated[int, Ge(0)] | None = None
    # Specifies the checksum of the PE binary.
    checksum_hex: str | None = None
    # Specifies the subsystem (e.g., GUI, device driver, etc.) that is required to run this image.
    subsystem_hex: str | None = None
    # Specifies the flags that characterize the PE binary.
    dll_characteristics_hex: str | None = None
    # Specifies the size of the stack to reserve, in bytes.
    size_of_stack_reserve: Annotated[int, Ge(0)] | None = None
    # Specifies the size of the stack to commit, in bytes.
    size_of_stack_commit: Annotated[int, Ge(0)] | None = None
    # Specifies the size of the local heap space to reserve, in bytes.
    size_of_heap_reserve: Annotated[int, Ge(0)] | None = None
    # Specifies the size of the local heap space to commit, in bytes.
    size_of_heap_commit: Annotated[int, Ge(0)] | None = None
    # Specifies the reserved loader flags.
    loader_flags_hex: str | None = None
    # Specifies the number of data-directory entries in the remainder of the optional header.
    number_of_rva_and_sizes: int | None = None
    # Specifies any hashes that were computed for the optional header.
    hashes: Hashes | None = None

    # Use common validator to avoid code duplication
    _at_least_one = create_at_least_one_property_validator()


# 6.7.6 Windows PE Binary File Extension
class WindowsPEBinaryExtension(Extension):
    """
    The Windows™ PE Binary File extension specifies a default extension for capturing properties specific to
    Windows portable executable (PE) files.

    The key for this extension when used in the extensions dictionary MUST be windows-pebinary-ext.
    Note that this predefined extension does not use the extension facility described in section 7.3.

    An object using the Windows™ PE Binary File Extension MUST contain at least one property other than the
    required pe_type property from this extension.
    """

    # Specifies the type of the PE binary.
    # This is an open vocabulary and values SHOULD come from the windows-pebinary-type-ov open vocabulary.
    pe_type: str
    # Specifies the special import hash, or 'imphash', calculated for the PE Binary based on its imported
    # libraries and functions.
    imphash: str | None = None
    # Specifies the type of target machine.
    machine_hex: str | None = None
    # Specifies the number of sections in the PE binary, as a non-negative integer.
    number_of_sections: Annotated[int, Ge(0)] | None = None
    # Specifies the time when the PE binary was created.
    # The timestamp value MUST be precise to the second.
    time_date_stamp: datetime | None = None
    # Specifies the file offset of the COFF symbol table.
    pointer_to_symbol_table_hex: str | None = None
    # Specifies the number of entries in the symbol table of the PE binary, as a non-negative integer.
    number_of_symbols: Annotated[int, Ge(0)] | None = None
    # Specifies the size of the optional header of the PE binary.
    size_of_optional_header: Annotated[int, Ge(0)] | None = None
    # Specifies the flags that indicate the file’s characteristics.
    characteristics_hex: str | None = None
    # Specifies any hashes that were computed for the file header.
    file_header_hashes: Hashes | None = None
    # Specifies the PE optional header of the PE binary.
    optional_header: WindowsPEOptionalHeader | None = None
    # Specifies metadata about the sections in the PE file.
    sections: list[WindowsPESection] | None = None


FileExtensions = TypedDict(
    "FileExtensions",
    {
        "archive-ext": ArchiveFileExtension,
        "ntfs-ext": NTFSFileExtension,
        "pdf-ext": PDFFileExtension,
        "raster-image-ext": RasterImageFileExtension,
        "windows-pebinary-ext": WindowsPEBinaryExtension,
    },
    total=False,
    extra_items=SerializeAsAny[Extension],
)


# 6.7 File Object
class File(StixObservable):
    """
    The File object represents the properties of a file.
    """

    type: Literal["file"] = "file"  # pyright: ignore[reportIncompatibleVariableOverride]
    # The File object defines the following extensions. In addition to these, producers MAY create their own.
    # Dictionary keys MUST use the specification defined name (examples above) or be the id of a STIX Extension object,
    # depending on the type of extension being used.
    # The corresponding dictionary values MUST contain the contents of the extension instance.
    extensions: FileExtensions | None = None  # pyright: ignore[reportIncompatibleVariableOverride]
    # Specifies a dictionary of hashes for the file.
    # When used with the Archive File Extension, this refers to the hash of the entire archive file, not its contents.
    hashes: Hashes | None = None
    # Specifies the size of the file, in bytes.
    size: Annotated[int, Ge(0)] | None = None
    # Specifies the name of the file.
    name: str | None = None
    # Specifies the observed encoding for the name of the file. This value MUST be specified using the corresponding
    # name from the 2013-12-20 revision of the IANA character set registry [Character Sets]. If the value from the
    # Preferred MIME Name column for a character set is defined, this value MUST be used; if it is not defined, then
    # the value from the Name column in the registry MUST be used instead.
    # This property allows for the capture of the original text encoding for the file name, which may be forensically
    # relevant; for example, a file on an NTFS volume whose name was created using the windows-1251 encoding, commonly
    # used for languages based on Cyrillic script.
    name_enc: str | None = None
    # Specifies the hexadecimal constant ("magic number") associated with a specific file format that corresponds
    # to the file, if applicable.
    magic_number_hex: str | None = None
    # Specifies the MIME type name specified for the file, e.g., application/msword.
    # Whenever feasible, this value SHOULD be one of the values defined in the Template column in the IANA media type
    # registry [Media Types].
    # Maintaining a comprehensive universal catalog of all extant file types is obviously not possible. When specifying
    # a MIME Type not included in the IANA registry, implementers should use their best judgement so as to facilitate
    # interoperability.
    mime_type: str | None = None
    # Specifies the date/time the file was created.
    ctime: datetime | None = None
    # Specifies the date/time the file was last written to/modified.
    mtime: datetime | None = None
    # Specifies the date/time the file was last accessed.
    atime: datetime | None = None
    # Specifies the parent directory of the file, as a reference to a Directory object.
    parent_directory_ref: Identifier | None = None
    # Specifies a list of references to other Cyber-observable Objects contained within the file, such as another file
    # that is appended to the end of the file, or an IP address that is contained somewhere in the file.
    # This is intended for use cases other than those targeted by the Archive extension.
    contains_refs: list[Identifier] | None = None
    # Specifies the content of the file, represented as an Artifact object.
    content_ref: Identifier | None = None

    @model_validator(mode="after")
    def at_least_one_of(self) -> Self:
        """
        A File object MUST contain at least one of hashes or name.
        """
        if self.hashes is None and self.name is None:
            raise ValueError("At least one of hashes or name must be present.")
        return self

    class Config:
        json_schema_extra: dict[str, list[str]] = {
            "id_contributing_properties": [
                "hashes",
                "name",
                "extensions",
                "parent_directory_ref",
            ]
        }


# 6.8 IPv4 Address Object
class IPv4Address(StixObservable):
    """
    The IPv4 Address object represents one or more IPv4 addresses expressed using CIDR notation.
    """

    type: Literal["ipv4-addr"] = "ipv4-addr"  # pyright: ignore[reportIncompatibleVariableOverride]
    # Specifies the values of one or more IPv4 addresses expressed using CIDR notation.
    # If a given IPv4 Address object represents a single IPv4 address, the CIDR /32 suffix MAY be omitted.
    value: ipaddress.IPv4Address | ipaddress.IPv4Network
    # Specifies a list of references to one or more Layer 2 Media Access Control (MAC) addresses that the IPv4
    # address resolves to.
    resolves_to_refs: list[Identifier] | None = None
    # Specifies a list of references to one or more autonomous systems (AS) that the IPv4 address belongs to.
    belongs_to_refs: list[Identifier] | None = None

    class Config:
        json_schema_extra: dict[str, list[str]] = {
            "id_contributing_properties": ["value"]
        }


# 6.9 IPv6 Address Object
class IPv6Address(StixObservable):
    """
    The IPv6 Address object represents one or more IPv6 addresses expressed using CIDR notation.
    """

    type: Literal["ipv6-addr"] = "ipv6-addr"  # pyright: ignore[reportIncompatibleVariableOverride]
    # Specifies the values of one or more IPv6 addresses expressed using CIDR notation.
    # If a given IPv6 Address object represents a single IPv6 address, the CIDR /128 suffix MAY be omitted.
    value: ipaddress.IPv6Address | ipaddress.IPv6Network
    # Specifies a list of references to one or more Layer 2 Media Access Control (MAC) addresses that the IPv6
    # address resolves to.
    resolves_to_refs: list[Identifier] | None = None
    # Specifies a list of references to one or more autonomous systems (AS) that the IPv6 address belongs to.
    belongs_to_refs: list[Identifier] | None = None

    class Config:
        json_schema_extra: dict[str, list[str]] = {
            "id_contributing_properties": ["value"]
        }


# 6.10 MAC Address Object
class MACAddress(StixObservable):
    """
    The MAC Address object represents a single Media Access Control (MAC) address.
    """

    type: Literal["mac-addr"] = "mac-addr"  # pyright: ignore[reportIncompatibleVariableOverride]
    # Specifies the value of a single MAC address.
    # The MAC address value MUST be represented as a single colon-delimited, lowercase MAC-48 address, which MUST
    # include leading zeros for each octet.
    # TODO: check the following regex: ^([0-9a-f]{2}:){5}[0-9a-f]{2}$
    value: str

    class Config:
        json_schema_extra: dict[str, list[str]] = {
            "id_contributing_properties": ["value"]
        }


# 6.11 Mutex Object
class Mutex(StixObservable):
    """
    The Mutex object represents the properties of a mutual exclusion (mutex) object.
    """

    type: Literal["mutex"] = "mutex"  # pyright: ignore[reportIncompatibleVariableOverride]
    # Specifies the name of the mutex object.
    name: str

    class Config:
        json_schema_extra: dict[str, list[str]] = {
            "id_contributing_properties": ["name"]
        }


# 6.12.2 HTTP Request Extension
class HTTPRequestExtension(Extension):
    """
    The HTTP request extension specifies a default extension for capturing network traffic properties specific to
    HTTP requests.

    The key for this extension when used in the extensions dictionary MUST be http-request-ext.
    Note that this predefined extension does not use the extension facility described in section 7.3.
    The corresponding protocol value for this extension is http.
    """

    # Specifies the HTTP method portion of the HTTP request line, as a lowercase string.
    request_method: str
    # Specifies the value (typically a resource path) portion of the HTTP request line.
    request_value: str
    # Specifies the HTTP version portion of the HTTP request line, as a lowercase string.
    request_version: str | None = None
    # Specifies all of the HTTP header fields that may be found in the HTTP client request, as a dictionary.
    request_header: dict[str, list[str]] | None = None
    # Specifies the length of the HTTP message body, if included, in bytes.
    message_body_length: int | None = None
    # Specifies the data contained in the HTTP message body, if included.
    message_body_data_ref: Identifier | None = None


# 6.12.3 ICMP Extension
class ICMPExtension(Extension):
    """
    The ICMP extension specifies a default extension for capturing network traffic properties specific to ICMP.

    The key for this extension when used in the extensions dictionary MUST be icmp-ext.
    Note that this predefined extension does not use the extension facility described in section 7.3.
    The corresponding protocol value for this extension is icmp.
    """

    # Specifies the ICMP type byte.
    icmp_type_hex: str
    # Specifies the ICMP code byte.
    icmp_code_hex: str


# 6.12.4 Network Socket Extension
class NetworkSocketExtension(Extension):
    """
    The Network Socket extension specifies a default extension for capturing network traffic properties associated
    with network sockets.

    The key for this extension when used in the extensions dictionary MUST be socket-ext.
    Note that this predefined extension does not use the extension facility described in section 7.3.
    """

    # Specifies the address family (AF_*) that the socket is configured for.
    address_family: NetworkSocketAddressFamily
    # Specifies whether the socket is in blocking mode.
    is_blocking: bool | None = None
    # Specifies whether the socket is in listening mode.
    is_listening: bool | None = None
    # Specifies any options (e.g., SO_*) that may be used by the socket, as a dictionary.
    # Each key in the dictionary SHOULD be a case-preserved version of the option name, e.g., SO_ACCEPTCONN.
    # Each key value in the dictionary MUST be the value for the corresponding options key.
    # Each dictionary value MUST be an integer. For SO_RCVTIMEO, SO_SNDTIMEO and SO_LINGER the value represents
    # the number of milliseconds. If the SO_LINGER key is present, it indicates that the SO_LINGER option is active.
    options: dict[str | int, int] | None = None
    # Specifies the type of the socket.
    socket_type: NetworkSocketType | None = None
    # Specifies the socket file descriptor value associated with the socket, as a non-negative integer.
    socket_descriptor: int | None = None
    # Specifies the handle or inode value associated with the socket.
    socket_handle: int | None = None


# 6.12.5 TCP Extension
class TCPExtension(Extension):
    """
    The TCP extension specifies a default extension for capturing network traffic properties specific to TCP.
    An object using the TCP Extension MUST contain at least one property from this extension.
    """

    # Specifies the source TCP flags, as the union of all TCP flags observed between the start of the traffic
    # (as defined by the start property) and the end of the traffic (as defined by the end property).
    # If the start and end times of the traffic are not specified, this property SHOULD be interpreted as the union
    # of all TCP flags observed over the entirety of the network traffic being reported upon.
    src_flags_hex: str | None = None
    # Specifies the destination TCP flags, as the union of all TCP flags observed between the start of the traffic
    # (as defined by the start property) and the end of the traffic (as defined by the end property).
    # If the start and end times of the traffic are not specified, this property SHOULD be interpreted as the union
    # of all TCP flags observed over the entirety of the network traffic being reported upon.
    dst_flags_hex: str | None = None

    @model_validator(mode="after")
    def at_least_one_of(self) -> Self:
        """
        An object using the TCP Extension MUST contain at least one property from this extension.
        """
        if self.src_flags_hex is None and self.dst_flags_hex is None:
            raise ValueError("At least one property must be present")
        return self


NetworkTrafficExtensions = TypedDict(
    "NetworkTrafficExtensions",
    {
        "http-request-ext": HTTPRequestExtension,
        "icmp-ext": ICMPExtension,
        "socket-ext": NetworkSocketExtension,
        "tcp-ext": TCPExtension,
    },
    total=False,
    extra_items=SerializeAsAny[Extension],
)


# 6.12 Network Traffic Object
class NetworkTraffic(StixObservable):
    """
    The Network Traffic object represents arbitrary network traffic that originates from a source and is addressed to
    a destination. The network traffic MAY or MAY NOT constitute a valid unicast, multicast, or broadcast network
    connection. This MAY also include traffic that is not established, such as a SYN flood.

    To allow for use cases where a source or destination address may be sensitive and not suitable for sharing,
    such as addresses that are internal to an organization's network, the source and destination properties
    (src_ref and dst_ref, respectively) are defined as optional in the properties table below.
    """

    type: Literal["network-traffic"] = "network-traffic"  # pyright: ignore[reportIncompatibleVariableOverride]
    # The Network Traffic object defines the following extensions. In addition to these, producers MAY create their own.
    # Dictionary keys MUST use the specification defined name (examples above) or be the id of a STIX Extension object,
    # depending on the type of extension being used.
    # The corresponding dictionary values MUST contain the contents of the extension instance.
    extensions: NetworkTrafficExtensions | None = None  # pyright: ignore[reportIncompatibleVariableOverride]
    # Specifies the date/time the network traffic was initiated, if known.
    start: datetime | None = None
    # Specifies the date/time the network traffic ended, if known.
    end: datetime | None = None
    # Indicates whether the network traffic is still ongoing.
    is_active: bool | None = None
    # Specifies the source of the network traffic, as a reference to a Cyber-observable Object.
    # The object referenced MUST be of type ipv4-addr, ipv6-addr, mac-addr, or domain-name
    # (for cases where the IP address for a domain name is unknown).
    src_ref: Identifier | None = None
    # Specifies the destination of the network traffic, as a reference to a Cyber-observable Object.
    # The object referenced MUST be of type ipv4-addr, ipv6-addr, mac-addr, or domain-name
    # (for cases where the IP address for a domain name is unknown).
    dst_ref: Identifier | None = None
    # Specifies the source port used in the network traffic, as an integer.
    src_port: Annotated[int, Ge(0), Le(65535)] | None = None
    # Specifies the destination port used in the network traffic, as an integer.
    dst_port: Annotated[int, Ge(0), Le(65535)] | None = None
    # Specifies the protocols observed in the network traffic, along with their corresponding state.
    # Protocols MUST be listed in low to high order, from outer to inner in terms of packet encapsulation.
    # That is, the protocols in the outer level of the packet, such as IP, MUST be listed first.
    # The protocol names SHOULD come from the service names defined in the Service Name column of the
    # IANA Service Name and Port Number Registry [Port Numbers].
    # In cases where there is variance in the name of a network protocol not included in the IANA Registry,
    # content producers should exercise their best judgement, and it is recommended that lowercase names be used for
    # consistency with the IANA registry.
    # If the protocol extension is present, the corresponding protocol value for that extension
    # SHOULD be listed in this property.
    protocols: list[str]
    # Specifies the number of bytes, as a positive integer, sent from the source to the destination.
    src_byte_count: Annotated[int, Ge(0)] | None = None
    # Specifies the number of bytes, as a positive integer, sent from the destination to the source.
    dst_byte_count: Annotated[int, Ge(0)] | None = None
    # Specifies the number of packets, as a positive integer, sent from the source to the destination.
    src_packets: Annotated[int, Ge(0)] | None = None
    # Specifies the number of packets, as a positive integer, sent from the destination to the source.
    dst_packets: Annotated[int, Ge(0)] | None = None
    # Specifies any IP Flow Information Export [IPFIX] data for the traffic, as a dictionary.
    # Each key/value pair in the dictionary represents the name/value of a single IPFIX element.
    # Accordingly, each dictionary key SHOULD be a case-preserved version of the IPFIX element name,
    # e.g., octetDeltaCount. Each dictionary value MUST be either an integer or a string,
    # as well as a valid IPFIX property.
    ipfix: dict[str, int | str] | None = None
    # Specifies the bytes sent from the source to the destination.
    src_payload_ref: Identifier | None = None
    # Specifies the bytes sent from the destination to the source.
    dst_payload_ref: Identifier | None = None
    # Links to other network-traffic objects encapsulated by this network-traffic object.
    encapsulates_refs: list[Identifier] | None = None
    # Links to another network-traffic object which encapsulates this object.
    encapsulated_by_ref: Identifier | None = None

    @model_validator(mode="after")
    def validate_end(self) -> Self:
        """
        If the end property and the start property are both defined, then this property
        MUST be greater than or equal to the timestamp in the start property.
        If the is_active property is true, then the end property MUST NOT be included.
        """
        if self.is_active and self.end is not None:
            raise ValueError(
                "The end property MUST NOT be included if is_active is true"
            )
        if self.start and self.end and self.start > self.end:
            raise ValueError("The end property MUST be greater than or equal to start")
        return self

    @model_validator(mode="after")
    def at_least_one_of(self) -> Self:
        """
        A Network Traffic object MUST contain the protocols property and at least one of the src_ref or dst_ref
        properties and SHOULD contain the src_port and dst_port properties.
        """
        if self.src_ref is None and self.dst_ref is None:
            raise ValueError("At least one of src_ref or dst_ref must be present")
        return self

    class Config:
        json_schema_extra: dict[str, list[str]] = {
            "id_contributing_properties": [
                "start",
                "end",
                "src_ref",
                "dst_ref",
                "src_port",
                "dst_port",
                "protocols",
                "extensions",
            ]
        }


# 6.13.2 Windows Process Extension
class WindowsProcessExtension(Extension):
    """
    The Windows Process extension specifies a default extension for capturing properties specific to Windows processes.

    The key for this extension when used in the extensions dictionary MUST be windows-process-ext.
    Note that this predefined extension does not use the extension facility described in section 7.3.
    """

    # Specifies whether Address Space Layout Randomization (ASLR) is enabled for the process.
    aslr_enabled: bool | None = None
    # Specifies whether Data Execution Prevention (DEP) is enabled for the process.
    dep_enabled: bool | None = None
    # Specifies the current priority class of the process in Windows.
    # This value SHOULD be a string that ends in _CLASS.
    priority: str | None = None
    # Specifies the Security ID (SID) value of the owner of the process.
    owner_sid: str | None = None
    # Specifies the title of the main window of the process.
    window_title: str | None = None
    # Specifies the STARTUP_INFO struct used by the process, as a dictionary.
    # Each name/value pair in the struct MUST be represented as a key/value pair in the dictionary,
    # where each key MUST be a case-preserved version of the original name.
    # For example, given a name of "lpDesktop" the corresponding key would be lpDesktop.
    startup_info: dict[str, JsonValue] | None = None
    # Specifies the Windows integrity level, or trustworthiness, of the process.
    integrity_level: WindowsIntegrityLevel | None = None

    @model_validator(mode="before")
    @classmethod
    def at_least_one(cls, data: Any) -> Any:  # pyright: ignore[reportExplicitAny, reportAny]
        """
        An object using the Windows Process Extension MUST contain at least one property from this extension.
        """
        if isinstance(data, dict):
            for key, value in data.items():  # pyright: ignore[reportUnknownVariableType]
                if key != "type" and value is not None:
                    return data  # pyright: ignore[reportUnknownVariableType]
            raise ValueError("At least one property must be present")
        raise TypeError("Input data must be a dictionary")


# 6.13.3 Windows Service Extension
class WindowsServiceExtension(Extension):
    """
    The Windows Service extension specifies a default extension for capturing properties specific to Windows services.

    The key for this extension when used in the extensions dictionary MUST be windows-service-ext.
    Note that this predefined extension does not use the extension facility described in section 7.3.
    """

    # Specifies the name of the service.
    service_name: str | None = None
    # Specifies the descriptions defined for the service.
    descriptions: list[str] | None = None
    # Specifies the display name of the service in Windows GUI controls.
    display_name: str | None = None
    # Specifies the name of the load ordering group of which the service is a member.
    group_name: str | None = None
    # Specifies the start options defined for the service.
    start_type: WindowsServiceStartType | None = None
    # Specifies the DLLs loaded by the service, as a reference to one or more File objects.
    service_dll_refs: list[Identifier] | None = None
    # Specifies the type of the service.
    service_type: WindowsServiceType | None = None
    # Specifies the current status of the service.
    service_status: WindowsServiceStatus | None = None

    @model_validator(mode="before")
    @classmethod
    def at_least_one(cls, data: Any) -> Any:  # pyright: ignore[reportExplicitAny, reportAny]
        """
        As all properties of this extension are optional, at least one of the properties defined below MUST be
        included when using this extension.
        """
        if isinstance(data, dict):
            for key, value in data.items():  # pyright: ignore[reportUnknownVariableType]
                if key != "type" and value is not None:
                    return data  # pyright: ignore[reportUnknownVariableType]
            raise ValueError("At least one property must be present")
        raise TypeError("Input data must be a dictionary")


ProcessExtensions = TypedDict(
    "ProcessExtensions",
    {
        "windows-service-ext": WindowsServiceExtension,
        "windows-process-ext": WindowsProcessExtension,
    },
    total=False,
    extra_items=SerializeAsAny[Extension],
)


# 6.13 Process Object
class Process(StixObservable):
    """
    The Process object represents common properties of an instance of a computer program as executed on an
    operating system. A Process object MUST contain at least one property (other than type) from this object
    (or one of its extensions).
    """

    type: Literal["process"] = "process"  # pyright: ignore[reportIncompatibleVariableOverride]
    # The Process object defines the following extensions. In addition to these, producers MAY create their own.
    # Dictionary keys MUST use the specification defined name (examples above) or be the id of a STIX Extension object,
    # depending on the type of extension being used.
    # The corresponding dictionary values MUST contain the contents of the extension instance.
    extensions: ProcessExtensions | None = None  # pyright: ignore[reportIncompatibleVariableOverride]
    # Specifies whether the process is hidden.
    is_hidden: bool | None = None
    # Specifies the Process ID, or PID, of the process.
    pid: int | None = None
    # Specifies the date/time at which the process was created.
    created_time: datetime | None = None
    # Specifies the current working directory of the process.
    cwd: str | None = None
    # Specifies the full command line used in executing the process, including the process name (which may be
    # specified individually via the image_ref.name property) and any arguments.
    command_line: str | None = None
    # Specifies the list of environment variables associated with the process as a dictionary.
    # Each key in the dictionary MUST be a case preserved version of the name of the environment variable,
    # and each corresponding value MUST be the environment variable value as a string.
    environment_variables: dict[str, str] | None = None
    # Specifies the list of network connections opened by the process, as a reference to one or more
    # Network Traffic objects.
    opened_connection_refs: list[Identifier] | None = None
    # Specifies the user that created the process, as a reference to a User Account object.
    creator_user_ref: Identifier | None = None
    # Specifies the executable binary that was executed as the process image, as a reference to a File object.
    image_ref: Identifier | None = None
    # Specifies the other process that spawned (i.e. is the parent of) this one, as a reference to a Process object.
    parent_ref: Identifier | None = None
    # Specifies the other processes that were spawned by (i.e. children of) this process, as a reference to one
    # or more other Process objects.
    child_refs: list[Identifier] | None = None

    @model_validator(mode="before")
    @classmethod
    def at_least_one(cls, data: Any) -> Any:  # pyright: ignore[reportExplicitAny, reportAny]
        """
        A Process object MUST contain at least one property (other than type)
        from this object (or one of its extensions).
        """
        if isinstance(data, dict):
            for key, value in data.items():  # pyright: ignore[reportUnknownVariableType]
                if key != "type" and value is not None:
                    return data  # pyright: ignore[reportUnknownVariableType]
            raise ValueError("At least one property must be present")
        raise TypeError("Input data must be a dictionary")


# 6.14 Software Object
class Software(StixObservable):
    """
    The Software object represents high-level properties associated with software, including software products.
    """

    type: Literal["software"] = "software"  # pyright: ignore[reportIncompatibleVariableOverride]
    # Specifies the name of the software.
    name: str
    # Specifies the Common Platform Enumeration (CPE) entry for the software, if available.
    # The value for this property MUST be a CPE v2.3 entry from the official NVD CPE Dictionary [NVD].
    # While the CPE dictionary does not contain entries for all software, whenever it does contain an identifier
    # for a given instance of software, this property SHOULD be present.
    cpe: str | None = None
    # Specifies the Software Identification (SWID) Tags [SWID] entry for the software, if available. The tag attribute,
    # tagId, a globally unique identifier, SHOULD be used as a proxy identifier of the tagged product.
    swid: str | None = None
    # Specifies the languages supported by the software. The value of each list member MUST be a language code
    # conformant to [RFC5646].
    languages: list[str] | None = None
    # Specifies the name of the vendor of the software.
    vendor: str | None = None
    # Specifies the version of the software.
    version: str | None = None

    class Config:
        json_schema_extra: dict[str, list[str]] = {
            "id_contributing_properties": ["name", "cpe", "swid", "vendor", "version"]
        }


# 6.15 URL Object
class URL(StixObservable):
    """
    The URL object represents the properties of a uniform resource locator (URL).
    """

    type: Literal["url"] = "url"  # pyright: ignore[reportIncompatibleVariableOverride]
    # Specifies the value of the URL. The value of this property MUST conform to [RFC3986], more specifically
    # section 1.1.3 with reference to the definition for "Uniform Resource Locator".
    value: StixUrl

    class Config:
        json_schema_extra: dict[str, list[str]] = {
            "id_contributing_properties": ["value"]
        }


# 6.16.2 UNIX Account Extension
class UnixAccountExtension(Extension):
    """
    The UNIX account extension specifies a default extension for capturing the additional information for an account
    on a UNIX system. The key for this extension when used in the extensions dictionary MUST be unix-account-ext.

    Note that this predefined extension does not use the extension facility described in Section 7.3.
    """

    # Specifies the primary group ID of the account.
    gid: int | None = None
    # Specifies a list of names of groups that the account is a member of.
    groups: list[str] | None = None
    # Specifies the home directory of the account.
    home_dir: str | None = None
    # Specifies the account’s command shell.
    shell: str | None = None

    @model_validator(mode="before")
    @classmethod
    def at_least_one(cls, data: Any) -> Any:  # pyright: ignore[reportExplicitAny, reportAny]
        """
        An object using the UNIX Account Extension MUST contain at least one property from this extension.
        """
        if isinstance(data, dict):
            for key, value in data.items():  # pyright: ignore[reportUnknownVariableType]
                if key != "type" and value is not None:
                    return data  # pyright: ignore[reportUnknownVariableType]
            raise ValueError("At least one property must be present")
        raise TypeError("Input data must be a dictionary")


UserAccountExtensions = TypedDict(
    "UserAccountExtensions",
    {"unix-account-ext": UnixAccountExtension},
    total=False,
    extra_items=SerializeAsAny[Extension],
)


# 6.16 User Account Object
class UserAccount(StixObservable):
    """
    The User Account object represents an instance of any type of user account, including but not limited to
    operating system, device, messaging service, and social media platform accounts.
    """

    type: Literal["user-account"] = "user-account"  # pyright: ignore[reportIncompatibleVariableOverride]
    # The User Account object defines the following extensions. In addition to these, producers MAY create their own.
    # Dictionary keys MUST use the specification defined name (examples above) or be the id of a STIX Extension object,
    # depending on the type of extension being used.
    # The corresponding dictionary values MUST contain the contents of the extension instance.
    extensions: UserAccountExtensions | None = None  # pyright: ignore[reportIncompatibleVariableOverride]
    # Specifies the identifier of the account. The format of the identifier depends on the system the user account is
    # maintained in, and may be a numeric ID, a GUID, an account name, an email address, etc. The user_id property
    # should be populated with whatever field is the unique identifier for the system the account is a member of.
    # For example, on UNIX systems it would be populated with the UID.
    user_id: str | None = None
    # Specifies a cleartext credential. This is only intended to be used in capturing metadata from malware analysis
    # (e.g., a hard-coded domain administrator password that the malware attempts to use for lateral movement) and
    # SHOULD NOT be used for sharing of PII.
    credential: str | None = None
    # Specifies the account login string, used in cases where the user_id property specifies something other than what
    # a user would type when they login.
    # For example, in the case of a Unix account with user_id 0, the account_login might be "root".
    account_login: str | None = None
    # Specifies the type of the account.
    # This is an open vocabulary and values SHOULD come from the account-type-ov open vocabulary.
    account_type: str | None = None
    # Specifies the display name of the account, to be shown in user interfaces, if applicable.
    # On Unix, this is equivalent to the GECOS field.
    display_name: str | None = None
    # Indicates that the account is associated with a network service or system process (daemon), not a
    # specific individual.
    is_service_account: bool | None = None
    # Specifies that the account has elevated privileges
    # (i.e., in the case of root on Unix or the Windows Administrator account).
    is_privileged: bool | None = None
    #  	Specifies that the account has the ability to escalate privileges
    # (i.e., in the case of sudo on Unix or a Windows Domain Admin account)
    can_escalate_privs: bool | None = None
    # Specifies if the account is disabled.
    is_disabled: bool | None = None
    # Specifies when the account was created.
    account_created: datetime | None = None
    # Specifies the expiration date of the account.
    account_expires: datetime | None = None
    # Specifies when the account credential was last changed.
    credential_last_changed: datetime | None = None
    # Specifies when the account was first accessed.
    account_first_login: datetime | None = None
    # Specifies when the account was last accessed.
    account_last_login: datetime | None = None

    @model_validator(mode="before")
    @classmethod
    def at_least_one(cls, data: Any) -> Any:  # pyright: ignore[reportExplicitAny, reportAny]
        """
        As all properties of this object are optional, at least one of the properties defined below
        MUST be included when using this object.
        """
        if isinstance(data, dict):
            for key, value in data.items():  # pyright: ignore[reportUnknownVariableType]
                if key != "type" and value is not None:
                    return data  # pyright: ignore[reportUnknownVariableType]
            raise ValueError("At least one property must be present")
        raise TypeError("Input data must be a dictionary")

    class Config:
        json_schema_extra: dict[str, list[str]] = {
            "id_contributing_properties": ["account_type", "user_id", "account_login"]
        }


# 6.17.2 Windows Registry Value Type
class WindowsRegistryValueType(StixCore):
    """
    The Windows Registry Value type captures the properties of a Windows Registry Key Value.
    """

    # Specifies the name of the registry value. For specifying the default value in a registry key,
    # an empty string MUST be used.
    name: str | None = None
    # Specifies the data contained in the registry value.
    data: str | None = None
    # Specifies the registry (REG_*) data type used in the registry value.
    data_type: WindowsRegistryDatatype | None = None

    @model_validator(mode="before")
    @classmethod
    def at_least_one(cls, data: Any) -> Any:  # pyright: ignore[reportExplicitAny, reportAny]
        """
        As all properties of this object are optional, at least one of the properties defined below
        MUST be included when using this object.
        """
        if isinstance(data, dict):
            for key, value in data.items():  # pyright: ignore[reportUnknownVariableType]
                if key != "type" and value is not None:
                    return data  # pyright: ignore[reportUnknownVariableType]
            raise ValueError("At least one property must be present")
        raise TypeError("Input data must be a dictionary")


# 6.17 Windows Registry Key Object
class WindowsRegistryKey(StixObservable):
    """
    The Registry Key object represents the properties of a Windows registry key.
    """

    type: Literal["windows-registry-key"] = "windows-registry-key"  # pyright: ignore[reportIncompatibleVariableOverride]
    # Specifies the full registry key including the hive.
    key: str | None = None
    # Specifies the values found under the registry key.
    # The value of the key, including the hive portion, SHOULD be case-preserved. The hive portion of the key MUST be
    # fully expanded and not truncated; e.g., HKEY_LOCAL_MACHINE must be used instead of HKLM.
    values: list[WindowsRegistryValueType] | None = None
    # Specifies the last date/time that the registry key was modified.
    modified_time: datetime | None = None
    # Specifies a reference to the user account that created the registry key.
    # The object referenced in this property MUST be of type user-account.
    creator_user_ref: Identifier | None = None
    # Specifies the number of subkeys contained under the registry key.
    number_of_subkeys: int | None = None

    @model_validator(mode="before")
    @classmethod
    def at_least_one(cls, data: Any) -> Any:  # pyright: ignore[reportExplicitAny, reportAny]
        """
        As all properties of this object are optional, at least one of the properties defined below
        MUST be included when using this object.
        """
        if isinstance(data, dict):
            for key, value in data.items():  # pyright: ignore[reportUnknownVariableType]
                if key != "type" and value is not None:
                    return data  # pyright: ignore[reportUnknownVariableType]
            raise ValueError("At least one property must be present")
        raise TypeError("Input data must be a dictionary")

    class Config:
        json_schema_extra: dict[str, list[str]] = {
            "id_contributing_properties": ["key", "values"]
        }


# 6.18.2 X.509 v3 Extensions Type
class X509v3ExtensionsType(Extension):
    """
    The X.509 v3 Extensions type captures properties associated with X.509 v3 extensions, which serve as a mechanism
    for specifying additional information such as alternative subject names.

    Note that the use of the term "extensions" in this context refers to the X.509 v3 Extensions type and is not a
    STIX Cyber Observables extension. Therefore, it is a type that describes X.509 extensions.
    """

    # Specifies a multi-valued extension which indicates whether a certificate is a CA certificate.
    # The first (mandatory) name is CA followed by TRUE or FALSE. If CA is TRUE, then an optional pathlen name
    # followed by a non-negative value can be included. Also equivalent to the object ID (OID) value of 2.5.29.19.
    basic_constraints: str | None = None
    # Specifies a namespace within which all subject names in subsequent certificates in a certification path
    # MUST be located. Also equivalent to the object ID (OID) value of 2.5.29.30.
    name_constraints: str | None = None
    # Specifies any constraints on path validation for certificates issued to CAs.
    # Also equivalent to the object ID (OID) value of 2.5.29.36.
    policy_constraints: str | None = None
    # Specifies a multi-valued extension consisting of a list of names of the permitted key usages.
    # Also equivalent to the object ID (OID) value of 2.5.29.15.
    key_usage: str | None = None
    # Specifies a list of usages indicating purposes for which the certificate public key can be used for.
    # Also equivalent to the object ID (OID) value of 2.5.29.37.
    extended_key_usage: str | None = None
    # Specifies the identifier that provides a means of identifying certificates that contain a particular public key.
    # Also equivalent to the object ID (OID) value of 2.5.29.14.
    subject_key_identifier: str | None = None
    # Specifies the identifier that provides a means of identifying the public key corresponding to the private key
    # used to sign a certificate. Also equivalent to the object ID (OID) value of 2.5.29.35.
    authority_key_identifier: str | None = None
    # Specifies the additional identities to be bound to the subject of the certificate.
    # Also equivalent to the object ID (OID) value of 2.5.29.17.
    subject_alternative_name: str | None = None
    # Specifies the additional identities to be bound to the issuer of the certificate.
    # Also equivalent to the object ID (OID) value of 2.5.29.18.
    issuer_alternative_name: str | None = None
    # Specifies the identification attributes (e.g., nationality) of the subject.
    # Also equivalent to the object ID (OID) value of 2.5.29.9.
    subject_directory_attributes: str | None = None
    # Specifies how CRL information is obtained.
    # Also equivalent to the object ID (OID) value of 2.5.29.31.
    crl_distribution_points: str | None = None
    # Specifies the number of additional certificates that may appear in the path before anyPolicy is no longer
    # permitted. Also equivalent to the object ID (OID) value of 2.5.29.54.
    inhibit_any_policy: str | None = None
    # Specifies the date on which the validity period begins for the private key, if it is different from the
    # validity period of the certificate.
    private_key_usage_period_not_before: datetime | None = None
    # Specifies the date on which the validity period ends for the private key, if it is different from the
    # validity period of the certificate.
    private_key_usage_period_not_after: datetime | None = None
    # Specifies a sequence of one or more policy information terms, each of which consists of an object identifier
    # (OID) and optional qualifiers. Also equivalent to the object ID (OID) value of 2.5.29.32.
    certificate_policies: str | None = None
    # Specifies one or more pairs of OIDs; each pair includes an issuerDomainPolicy and a subjectDomainPolicy.
    # The pairing indicates whether the issuing CA considers its issuerDomainPolicy equivalent to the subject
    # CA’s subjectDomainPolicy. Also equivalent to the object ID (OID) value of 2.5.29.33.
    policy_mappings: str | None = None

    @classmethod
    def at_least_one(cls, data: Any) -> Any:  # pyright: ignore[reportExplicitAny, reportAny]
        """
        An object using the X.509 v3 Extensions type MUST contain at least one property from this type.
        """
        if isinstance(data, dict):
            for key, value in data.items():  # pyright: ignore[reportUnknownVariableType]
                if key != "type" and value is not None:
                    return data  # pyright: ignore[reportUnknownVariableType]
            raise ValueError("At least one property must be present")
        raise TypeError("Input data must be a dictionary")


# 6.18 X.509 Certificate Object
class X509Certificate(StixObservable):
    """
    The X.509 Certificate object represents the properties of an X.509 certificate, as defined by ITU recommendation
    X.509 [X509].
    """

    type: Literal["x509-certificate"] = "x509-certificate"  # pyright: ignore[reportIncompatibleVariableOverride]
    # Specifies whether the certificate is self-signed, i.e., whether it is signed by the same entity whose
    # identity it certifies.
    is_self_signed: bool | None = None
    # Specifies any hashes that were calculated for the entire contents of the certificate.
    hashes: Hashes | None = None
    # Specifies the version of the encoded certificate.
    version: str | None = None
    # Specifies the unique identifier for the certificate, as issued by a specific Certificate Authority.
    serial_number: str | None = None
    # Specifies the name of the algorithm used to sign the certificate.
    signature_algorithm: str | None = None
    # Specifies the name of the Certificate Authority that issued the certificate.
    issuer: str | None = None
    # Specifies the date on which the certificate validity period begins.
    validity_not_before: datetime | None = None
    # Specifies the date on which the certificate validity period ends.
    validity_not_after: datetime | None = None
    # Specifies the name of the entity associated with the public key stored in the subject public key field of the
    # certificate.
    subject: str | None = None
    # Specifies the name of the algorithm with which to encrypt data being sent to the subject.
    subject_public_key_algorithm: str | None = None
    # Specifies the modulus portion of the subject's public RSA key.
    subject_public_key_modulus: str | None = None
    # Specifies the exponent portion of the subject's public RSA key, as an integer.
    subject_public_key_exponent: int | None = None
    # Specifies any standard X.509 v3 extensions that may be used in the certificate.
    x509_v3_extensions: X509v3ExtensionsType | None = None

    @classmethod
    def at_least_one(cls, data: Any) -> Any:  # pyright: ignore[reportExplicitAny, reportAny]
        """
        An X.509 Certificate object MUST contain at least one object specific property (other than type)
        from this object.
        """
        if isinstance(data, dict):
            for key, value in data.items():  # pyright: ignore[reportUnknownVariableType]
                if key != "type" and value is not None:
                    return data  # pyright: ignore[reportUnknownVariableType]
            raise ValueError("At least one property must be present")
        raise TypeError("Input data must be a dictionary")

    class Config:
        json_schema_extra: dict[str, list[str]] = {
            "id_contributing_properties": ["hashes", "serial_number"]
        }


SCOs = Annotated[
    (
        Artifact
        | AutonomousSystem
        | Directory
        | DomainName
        | EmailAddress
        | EmailMessage
        | File
        | IPv4Address
        | IPv6Address
        | MACAddress
        | Mutex
        | NetworkTraffic
        | Process
        | Software
        | URL
        | UserAccount
        | WindowsRegistryKey
        | X509Certificate
    ),
    Field(discriminator="type"),
]
