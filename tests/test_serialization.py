import json
from datetime import datetime
from ipaddress import ip_network
from pathlib import Path
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
from stidantic.types import StixCommon

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
}


class TestStixDeserialization(TestCase):
    def test_valid_bundle(self) -> None:
        with Path("tests/data/valid.json").open() as file:
            data = file.read()
        bundle = StixBundle.model_validate_json(data)
        for obj in bundle.objects:
            self.assertTrue(isinstance(obj, STIX_OBJECT_MAP.get(obj.type, StixCommon)))

    def test_valid_objects(self) -> None:
        with Path("tests/data/valid.json").open() as file:
            data = json.loads(file.read())

        for obj in data["objects"]:
            STIX_OBJECT_MAP.get(obj["type"], StixCommon).model_validate(obj)


class TestStixSerialization(TestCase):
    def test_valid_bundle_serialization(self) -> None:
        with Path("tests/data/valid.json").open() as file:
            data = json.loads(file.read())
        bundle = StixBundle.model_validate(data).model_dump(mode="json", exclude_none=True, by_alias=True)
        diff = DeepDiff(data, bundle)
        diff_dict = diff.to_dict()

        for key, value in diff["values_changed"].items():
            try:
                datetime.fromisoformat(value["old_value"])
                diff_dict["values_changed"].pop(key)
            except ValueError:
                pass
            try:
                ip_network(value["old_value"])
                diff_dict["values_changed"].pop(key)
            except ValueError:
                pass

        self.assertDictEqual({}, {k: v for k, v in diff_dict.items() if v})
