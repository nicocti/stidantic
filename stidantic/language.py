from datetime import datetime
from typing import Literal
from stidantic.types import Identifier, StixLanguage


# 7.1 Language Content
class LanguageContent(StixLanguage):
    type: Literal["language-content"] = "language-content"  # pyright: ignore[reportIncompatibleVariableOverride]
    # The object_ref property identifies the id of the object that this Language Content applies to.
    # It MUST be the identifier for a STIX Object.
    object_ref: Identifier
    # The object_modified property identifies the modified time of the object that this Language Content applies to.
    # It MUST be an exact match for the modified time of the STIX Object being referenced.
    object_modified: datetime | None = None
    # The contents property contains the actual Language Content (translation).
    # The keys in the dictionary MUST be RFC 5646 language codes for which language content is being provided [RFC5646].
    # The values each consist of a dictionary that mirrors the properties in the target object
    # (identified by object_ref and object_modified). For example, to provide a translation of the name property
    # on the target object the key in the dictionary would be name.
    # For each key in the nested dictionary:
    # ●      If the original property is a string, the corresponding property in the language content object
    # MUST contain a string with the content for that property in the language of the top-level key.
    # ●      If the original property is a list, the corresponding property in the translation object must also be
    # a list. Each item in this list recursively maps to the item at the same position in the list contained in the
    # target object. The lists MUST have the same length.
    # ●      In the event that translations are only provided for some list items, the untranslated list items MUST
    # be represented by an empty string (""). This indicates to a consumer of the Language Content object that they
    # should interpolate the translated list items in the Language Content object with the corresponding (untranslated)
    # list items from the original object as indicated by the object_ref property.
    # ●      If the original property is an object (including dictionaries), the corresponding location in the
    # translation object must also be an object. Each key/value field in this object recursively maps to the object
    # with the same key in the original.
    # The translation object MAY contain only a subset of the translatable fields of the original. Keys that point to
    # non-translatable properties in the target or to properties that do not exist in the target object MUST be ignored.
    contents: dict[str, dict[str, str]]
