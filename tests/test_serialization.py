import json
from datetime import datetime
from ipaddress import ip_network
from pathlib import Path
from typing import Any, Literal, override
from unittest import TestCase

from deepdiff import DeepDiff

from stidantic.bundle import StixBundle
from stidantic.extension import ExtensionDefinition
from stidantic.language import LanguageContent
from stidantic.marking import MarkingDefinition
from stidantic.sco import (
    URL,
    Artifact,
    AutonomousSystem,
    Directory,
    DomainName,
    EmailAddress,
    EmailMessage,
    File,
    IPv4Address,
    IPv6Address,
    MACAddress,
    Mutex,
    NetworkTraffic,
    Process,
    Software,
    UserAccount,
    WindowsRegistryKey,
    X509Certificate,
)
from stidantic.sdo import (
    AttackPattern,
    Campaign,
    CourseOfAction,
    Grouping,
    Identity,
    Incident,
    Indicator,
    Infrastructure,
    IntrusionSet,
    Location,
    Malware,
    MalwareAnalysis,
    Note,
    ObservedData,
    Opinion,
    Report,
    ThreatActor,
    Tool,
    Vulnerability,
)
from stidantic.sro import Relationship, Sighting
from stidantic.types import StixDomain, StixObservable


# pyright: reportAny=false, reportExplicitAny=false
class MyFavoriteSDO(StixDomain):
    type: Literal["my-favorite-sdo"] = "my-favorite-sdo"  # pyright: ignore[reportIncompatibleVariableOverride]
    name: str
    some_property_name1: str | None = None
    some_property_name2: str | None = None


class MyFavoriteSCO(StixObservable):
    type: Literal["my-favorite-sco"] = "my-favorite-sco"  # pyright: ignore[reportIncompatibleVariableOverride]
    name: str
    some_network_protocol_field: str | None = None


STIX_OBJECT_MAP = {
    "attack-pattern": AttackPattern,
    "campaign": Campaign,
    "course-of-action": CourseOfAction,
    "grouping": Grouping,
    "identity": Identity,
    "incident": Incident,
    "indicator": Indicator,
    "infrastructure": Infrastructure,
    "intrusion-set": IntrusionSet,
    "location": Location,
    "malware": Malware,
    "malware-analysis": MalwareAnalysis,
    "note": Note,
    "observed-data": ObservedData,
    "opinion": Opinion,
    "report": Report,
    "threat-actor": ThreatActor,
    "tool": Tool,
    "vulnerability": Vulnerability,
    "relationship": Relationship,
    "sighting": Sighting,
    "artifact": Artifact,
    "autonomous-system": AutonomousSystem,
    "directory": Directory,
    "domain-name": DomainName,
    "email-addr": EmailAddress,
    "email-message": EmailMessage,
    "file": File,
    "ipv4-addr": IPv4Address,
    "ipv6-addr": IPv6Address,
    "mac-addr": MACAddress,
    "mutex": Mutex,
    "network-traffic": NetworkTraffic,
    "process": Process,
    "software": Software,
    "url": URL,
    "user-account": UserAccount,
    "windows-registry-key": WindowsRegistryKey,
    "x509-certificate": X509Certificate,
    "marking-definition": MarkingDefinition,
    "language-content": LanguageContent,
    "extension-definition": ExtensionDefinition,
    "bundle": StixBundle,
    "my-favorite-sdo": MyFavoriteSDO,
    "my-favorite-sco": MyFavoriteSCO,
}


class TestStixDeserialization(TestCase):
    @override
    def setUp(self) -> None:
        sdo_extension_definition_data = {
            "id": "extension-definition--9c59fd79-4215-4ba2-920d-3e4f320e1e62",
            "type": "extension-definition",
            "spec_version": "2.1",
            "name": "New SDO 1",
            "description": "This schema creates a new object type called my-favorite-sdo-1",
            "created": "2014-02-20T09:16:08.989000Z",
            "modified": "2014-02-20T09:16:08.989000Z",
            "created_by_ref": "identity--11b76a96-5d2b-45e0-8a5a-f6994f370731",
            "schema": "https://www.example.com/schema-my-favorite-sdo-1/v1/",
            "version": "1.2.1",
            "extension_types": ["new-sdo"],
        }
        sdo_extension_definition = ExtensionDefinition.model_validate(sdo_extension_definition_data)
        sco_extension_definition_data = {
            "id": "extension-definition--c5333451-c08c-4c48-be5e-9ad4c947776a",
            "type": "extension-definition",
            "spec_version": "2.1",
            "name": "Extension My Favorite SDO and Sub-Comp",
            "description": "This schema adds a new object my-favorite-sdo and some sub-component to existing objects",
            "created": "2014-02-20T09:16:08.989000Z",
            "modified": "2014-02-20T09:16:08.989000Z",
            "created_by_ref": "identity--c1694394-c150-4f80-a69a-59ca5e850df4",
            "schema": "https://www.example.com/schema-newobj-subcomp/v1/schema.json",
            "version": "1.2.1",
            "extension_types": ["new-sdo", "new-sco", "property-extension"],
        }

        sco_extension_definition = ExtensionDefinition.model_validate(sco_extension_definition_data)
        StixBundle.register_new_object(definition=sdo_extension_definition, extension=MyFavoriteSDO)
        StixBundle.register_new_object(definition=sco_extension_definition, extension=MyFavoriteSCO)

    def test_valid_bundle(self) -> None:
        with Path("tests/data/valid.json").open() as file:
            data = file.read()
        bundle = StixBundle.model_validate_json(data)
        for obj in bundle.objects:
            self.assertTrue(isinstance(obj, STIX_OBJECT_MAP[obj.type]))

    def test_valid_objects(self) -> None:
        with Path("tests/data/valid.json").open() as file:
            data: dict[str, Any] = json.loads(file.read())

        for obj in data["objects"]:
            _parsed = STIX_OBJECT_MAP[obj["type"]].model_validate(obj)


class TestStixSerialization(TestCase):
    def test_valid_bundle_serialization(self) -> None:
        with Path("tests/data/valid.json").open() as file:
            data = json.loads(file.read())
        bundle = StixBundle.model_validate(data).model_dump(mode="json", exclude_none=True, by_alias=True)
        diff = DeepDiff(data, bundle)
        diff_dict: dict[str, Any] = diff.to_dict()  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]

        for key, value in diff["values_changed"].items():  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
            try:
                _parsed = datetime.fromisoformat(value["old_value"])  # pyright: ignore[reportUnknownArgumentType]
                diff_dict["values_changed"].pop(key)
            except ValueError:
                pass
            try:
                _parsed = ip_network(value["old_value"])  # pyright: ignore[reportUnknownArgumentType]
                diff_dict["values_changed"].pop(key)
            except ValueError:
                pass

        self.assertDictEqual({}, {k: v for k, v in diff_dict.items() if v})
