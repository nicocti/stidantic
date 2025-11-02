# stidantic [WIP]

**This is work in progress, not compliant yet.**

A Pydantic-based Python library for parsing, validating, and creating STIX 2.1 cyber threat intelligence data.

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Pydantic v2](https://img.shields.io/badge/pydantic-v2.12+-green.svg)](https://docs.pydantic.dev/)

## Overview

**stidantic** provides a type-safe, Pythonic way to work with [STIX 2.1](https://oasis-open.github.io/cti-documentation/stix/intro) (Structured Threat Information Expression) objects.

This library leverages [Pydantic](https://docs.pydantic.dev/) to provide:

- 🔒 **Strong type validation** for all STIX objects
- 📝 **IDE auto-completion** and type hints
- ✅ **Automatic validation** of STIX specification constraints
- 🔄 **Easy JSON serialization/deserialization**
- ❄️ **Immutable models** with frozen Pydantic configurations
- 🎯 **Discriminated unions** for polymorphic STIX object handling

## Installation

### Requirements

- Python 3.12 or later (uses PEP 695 type statements)
- Pydantic > 2.10

## Quick Start

### Parsing a STIX Bundle

```python
from stidantic.bundle import StixBundle

# Load from JSON file
with open("threat_data.json", "r") as f:
    bundle = StixBundle.model_validate_json(f.read())

# Access objects
print(f"Bundle contains {len(bundle.objects)} objects")
for obj in bundle.objects:
    print(f"- {obj.type}: {obj.id}")
```

### Creating STIX Objects

```python
from datetime import datetime
from stidantic.sdo import Campaign
from stidantic.types import Identifier

campaign = Campaign(
    id=Identifier("campaign--8e2e2d2b-17d4-4cbf-938f-98ee46b3cd3f"),
    created=datetime.now(),
    modified=datetime.now(),
    name="Operation Stealth",
    description="A sophisticated campaign targeting financial institutions",
    objective="Financial gain through wire fraud"
)

# Export to JSON
json_output = campaign.model_dump_json(indent=2, exclude_none=True, by_alias=True)
print(json_output)
```

## Implemented STIX Objects

### STIX Domain Objects (SDOs)
- ✅ `AttackPattern` - Ways adversaries attempt to compromise targets
- ✅ `Campaign` - Grouping of adversarial behaviors over time
- ✅ `Course of Action` - Action taken to prevent or respond to an attack
- ✅ `Grouping` - Explicitly asserts that STIX Objects have a shared context
- ✅ `Identity` - Actual individuals, organizations, or groups
- ✅ `Incident` - A stub object representing a security incident
- ✅ `Indicator` - Pattern that can be used to detect suspicious or malicious activity
- ✅ `Infrastructure` - Systems, software services, and associated resources
- ✅ `Intrusion Set` - A grouped set of adversarial behaviors and resources
- ✅ `Location` - A geographic location
- ✅ `Malware` - A type of TTP that represents malicious code
- ✅ `Malware Analysis` - The results of a malware analysis
- ✅ `Note` - Analyst-created content and context
- ✅ `Observed Data` - Information about cyber security related entities
- ✅ `Opinion` - An assessment of the correctness of a STIX Object
- ✅ `Report` - Collections of threat intelligence
- ✅ `Threat Actor` - Actual individuals, groups, or organizations
- ✅ `Tool` - Legitimate software that can be used by threat actors
- ✅ `Vulnerability` - A mistake in software that can be used to compromise a system

### STIX Cyber-observable Objects (SCOs)
- ✅ `Artifact` - Binary or file-like objects
- ✅ `AutonomousSystem` - Autonomous System (AS) information
- 🚧 `Directory` - A directory on a file system
- 🚧 `Domain Name` - A network domain name
- 🚧 `Email Address` - An email address
- 🚧 `Email Message` - An email message
- 🚧 `File` - A computer file
- 🚧 `IPv4 Address` - An IPv4 address
- 🚧 `IPv6 Address` - An IPv6 address
- 🚧 `MAC Address` - A Media Access Control (MAC) address
- 🚧 `Mutex` - A mutual exclusion object
- 🚧 `Network Traffic` - A network traffic flow
- 🚧 `Process` - A running process
- 🚧 `Software` - A software product
- 🚧 `URL` - A Uniform Resource Locator (URL)
- 🚧 `User Account` - A user account on a system
- 🚧 `Windows Registry Key` - A key in the Windows registry
- 🚧 `X.509 Certificate` - An X.509 certificate

### STIX Relationship Objects (SROs)
- ✅ `Relationship` - Connections between STIX objects
- ✅ `Sighting` - Observations of threat intelligence in the wild

### Meta Objects
- ✅ `MarkingDefinition` - Data markings (includes TLP)
- ✅ `LanguageContent` - Translations and internationalization
- ✅ `ExtensionDefinition` - Custom STIX extensions

### Bundle
- ✅ `StixBundle` - Container for STIX objects

## Roadmap

- **Full STIX 2.1 Compliance**
- **Python packaging**
- **Extensive Testing**
- Mind the datetime datatype serializer to follow the specification (convert to UTC).
- Better STIX Extension Support: Develop a robust and user-friendly mechanism for defining, parsing, and validating custom STIX extensions.
- TAXII 2.1 Server: Build a TAXII 2.1 compliant server using FastAPI.
- OCA Standard Extensions: Implement STIX extensions from the [Open Cybersecurity Alliance (OCA)](https://github.com/opencybersecurityalliance/stix-extensions) repository.
- Performance Tuning: Profile and optimize parsing and serialization.

## Resources

- [STIX 2.1 Specification](https://docs.oasis-open.org/cti/stix/v2.1/stix-v2.1.html)
- [STIX 2.1 Introduction](https://oasis-open.github.io/cti-documentation/stix/intro)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## License

stidantic is released under the [MIT License](https://opensource.org/licenses/MIT).

## Acknowledgments

This project implements the STIX 2.1 specification edited by Bret Jordan, Rich Piazza, and Trey Darley, published by the OASIS Cyber Threat Intelligence (CTI) Technical Committee.
