from typing import Annotated, Any, Literal, Self

from annotated_types import Ge, Le
from pydantic import Field
from pydantic.functional_validators import model_validator
from typing_extensions import deprecated

from stidantic.types import (
    ExternalReference,
    Identifier,
    KillChainPhase,
    StixDomain,
    StixTimestamp,
)
from stidantic.vocab import OpinionEnum


# 4.1 Attack Pattern
class AttackPattern(StixDomain):
    """
    Attack Patterns are a type of TTP that describe ways that adversaries attempt to compromise targets.

    Attack Patterns are used to help categorize attacks, generalize specific attacks to the patterns that they follow,
    and provide detailed information about how attacks are performed. An example of an attack pattern is
    "spear phishing": a common type of attack where an attacker sends a carefully crafted e-mail message
    to a party with the intent of getting them to click a link or open an attachment to deliver malware.

    Attack Patterns can also be more specific; spear phishing as practiced by a particular threat actor
    (e.g., they might generally say that the target won a contest) can also be an Attack Pattern.
    """

    type: Literal["attack-pattern"] = "attack-pattern"  # pyright: ignore[reportIncompatibleVariableOverride]
    # The name used to identify the Attack Pattern.
    name: str
    # A description that provides more details and context about the Attack Pattern,
    # potentially including its purpose and its key characteristics.
    description: str | None = None
    # Alternative names used to identify this Attack Pattern.
    aliases: list[str] | None = None
    # The list of kill chain phases for which this attack pattern is used.
    kill_chain_phases: list[KillChainPhase] | None = None


# 4.2 Campaign
class Campaign(StixDomain):
    """
    A Campaign is a grouping of adversarial behaviors that describes a set of malicious activities or attacks
    (sometimes called waves) that occur over a period of time against a specific set of targets.
    Campaigns usually have well defined objectives and may be part of an Intrusion Set.

    Campaigns are often attributed to an intrusion set and threat actors. The threat actors may reuse known
    infrastructure from the intrusion set or may set up new infrastructure specific for conducting that campaign.

    Campaigns can be characterized by their objectives and the incidents they cause, people or resources they target,
    and the resources (infrastructure, intelligence, Malware, Tools, etc.) they use.

    For example, a Campaign could be used to describe a crime syndicate's attack using a specific variant of
    malware and new C2 servers against the executives of ACME Bank during the summer of 2016 in order
    to gain secret information about an upcoming merger with another bank.
    """

    type: Literal["campaign"] = "campaign"  # pyright: ignore[reportIncompatibleVariableOverride]
    # A name used to identify the Campaign.
    name: str
    # A description that provides more details and context about the Campaign,
    # potentially including its purpose and its key characteristics.
    description: str | None = None
    # Alternative names used to identify this Campaign.
    aliases: list[str] | None = None
    # The time that this Campaign was first seen.
    # A summary property of data from sightings and other data that may or may not be available in STIX.
    # If new sightings are received that are earlier than the first seen timestamp,
    # the object may be updated to account for the new data.
    first_seen: StixTimestamp | None = None
    # The time that this Campaign was last seen.
    # A summary property of data from sightings and other data that may or may not be available in STIX.
    # If new sightings are received that are later than the last seen timestamp,
    # the object may be updated to account for the new data.
    last_seen: StixTimestamp | None = None
    # The Campaign’s primary goal, objective, desired outcome, or intended effect
    # — what the Threat Actor or Intrusion Set hopes to accomplish with this Campaign.
    objective: str | None = None

    @model_validator(mode="after")
    def validate_last_seen_after_first_seen(self) -> Self:
        """
        If the last_seen property and the first_seen property are both defined, then the last_seen property
        MUST be greater than or equal to the timestamp in the first_seen property.
        """
        if self.first_seen and self.last_seen and self.first_seen > self.last_seen:
            raise ValueError(
                "The last_seen property MUST be greater than or equal to the timestamp in the first_seen property"
            )
        return self


# 4.3 Course of Action
class CourseOfAction(StixDomain):
    """
    Note: The Course of Action object in STIX 2.1 is a stub. It is included to support basic use cases
    (such as sharing prose courses of action) but does not support the ability to represent automated courses of
    action or contain properties to represent metadata about courses of action. Future STIX 2 releases will expand it
    to include these capabilities.

    A Course of Action is an action taken either to prevent an attack or to respond to an attack that is in progress.
    It may describe technical, automatable responses (applying patches, reconfiguring firewalls) but can also describe
    higher level actions like employee training or policy changes. For example, a course of action to mitigate a
    vulnerability could describe applying the patch that fixes it.

    The Course of Action SDO contains a textual description of the action; a reserved action property also serves as a
    placeholder for future inclusion of machine automatable courses of action.
    """

    type: Literal["course-of-action"] = "course-of-action"  # pyright: ignore[reportIncompatibleVariableOverride]
    # A name used to identify the Course of Action.
    name: str
    # A description that provides more details and context about the Course of Action,
    # potentially including its purpose and its key characteristics.
    description: str | None = None
    # A reserved property that serves as a placeholder for future inclusion of machine automatable courses of action.
    # action: str | None = None


# 4.4 Grouping
class Grouping(StixDomain):
    """
    A Grouping object explicitly asserts that the referenced STIX Objects have a shared context, unlike a STIX Bundle
    (which explicitly conveys no context). A Grouping object should not be confused with an intelligence product,
    which should be conveyed via a STIX Report.

    A STIX Grouping object might represent a set of data that, in time, given sufficient analysis, would mature to
    convey an incident or threat report as a STIX Report object. For example, a Grouping could be used to characterize
    an ongoing investigation into a security event or incident. A Grouping object could also be used to assert that the
    referenced STIX Objects are related to an ongoing analysis process, such as when a threat analyst is collaborating
    with others in their trust community to examine a series of Campaigns and Indicators. The Grouping SDO contains a
    list of references to SDOs, SCOs, SROs, and SMOs, along with an explicit statement of the context shared by the
    content, a textual description, and the name of the grouping.
    """

    type: Literal["grouping"] = "grouping"  # pyright: ignore[reportIncompatibleVariableOverride]
    # A name used to identify the Grouping.
    name: str | None = None
    # A description that provides more details and context about the Grouping, potentially including its purpose and
    # its key characteristics.
    description: str | None = None
    # A short descriptor of the particular context shared by the content referenced by the Grouping.
    # The value for this property SHOULD come from the grouping-context-ov open vocabulary.
    context: str
    # Specifies the STIX Objects that are referred to by this Grouping.
    object_refs: list[Identifier]


# 4.5 Identity
class Identity(StixDomain):
    """
    Identities can represent actual individuals, organizations, or groups (e.g., ACME, Inc.) as well as classes of
    individuals, organizations, systems or groups (e.g., the finance sector).

    The Identity SDO can capture basic identifying information, contact information, and the sectors that the Identity
    belongs to. Identity is used in STIX to represent, among other things, targets of attacks, information sources,
    object creators, and threat actor identities.
    """

    type: Literal["identity"] = "identity"  # pyright: ignore[reportIncompatibleVariableOverride]
    # A name used to identify the Identity. When referring to a specific entity (e.g., an individual or organization),
    # this property SHOULD contain the canonical name of the specific entity.
    name: str
    # A description that provides more details and context about the Identity,
    # potentially including its purpose and its key characteristics.
    description: str | None = None
    # The list of roles that this Identity performs (e.g., CEO, Domain Administrators, Doctors, Hospital, or Retailer).
    # No open vocabulary is yet defined for this property.
    roles: list[str] | None = None
    # The type of entity that this Identity describes, e.g., an individual or organization.
    # The value for this property SHOULD come from the identity-class-ov open vocabulary.
    identity_class: str | None = None
    # The list of industry sectors that this Identity belongs to.
    # The value for this property SHOULD come from the industry-sector-ov open vocabulary.
    sectors: list[str] | None = None
    # The contact information (e-mail, phone number, etc.) for this Identity.
    # No format for this information is currently defined by this specification.
    contact_information: str | None = None


# 4.6 Incident
class Incident(StixDomain):
    """
    NOTE: The Incident object in STIX 2.1 is a stub. It is included to support basic use cases but does not contain
    properties to represent metadata about incidents. Future STIX 2 releases will expand it to include these
    capabilities. It is suggested that it is used as an extension point for an Incident object defined using the
    extension facility described in section 7.3.
    """

    type: Literal["incident"] = "incident"  # pyright: ignore[reportIncompatibleVariableOverride]
    # A name used to identify the Incident.
    name: str
    # A description that provides more details and context about the Incident,
    # potentially including its purpose and its key characteristics.
    description: str | None = None


class Indicator(StixDomain):
    """
    Indicators contain a pattern that can be used to detect suspicious or malicious cyber activity. For example, an
    Indicator may be used to represent a set of malicious domains and use the STIX Patterning Language
    (see section 9) to specify these domains.

    The Indicator SDO contains a simple textual description, the Kill Chain Phases that it detects behavior in, a time
    window for when the Indicator is valid or useful, and a required pattern property to capture a structured detection
    pattern. Conforming STIX implementations MUST support the STIX Patterning Language as defined in section 9.

    Relationships from the Indicator can describe the malicious or suspicious behavior that it directly detects
    (Malware, Tool, and Attack Pattern). In addition, it may also imply the presence of a Campaigns, Intrusion Sets,
    and Threat Actors, etc.
    """

    type: Literal["indicator"] = "indicator"  # pyright: ignore[reportIncompatibleVariableOverride]
    # A name used to identify the Indicator.
    # Producers SHOULD provide this property to help products and analysts understand what this Indicator actually does.
    name: str | None = None
    # A description that provides more details and context about the Indicator,
    # potentially including its purpose and its key characteristics.
    # Producers SHOULD provide this property to help products and analysts understand what this Indicator actually does.
    description: str | None = None
    # A set of categorizations for this indicator.
    # The values for this property SHOULD come from the indicator-type-ov open vocabulary.
    indicator_types: list[str] | None = None
    # The detection pattern for this Indicator MAY be expressed as a STIX Pattern as specified in section 9 or another
    # appropriate language such as SNORT, YARA, etc.
    pattern: str
    # The pattern language used in this indicator.
    # The value for this property SHOULD come from the pattern-type-ov open vocabulary.
    # The value of this property MUST match the type of pattern data included in the pattern property.
    pattern_type: str
    # The version of the pattern language that is used for the data in the pattern property which MUST match the type
    # of pattern data included in the pattern property.
    # For patterns that do not have a formal specification, the build or code version that the pattern is known to
    # work with SHOULD be used.
    # For the STIX Pattern language, the default value is determined by the specification version of the object.
    # For other languages, the default value SHOULD be the latest version of the patterning language at the time of
    # this object’s creation.
    pattern_version: str | None = None
    # The time from which this Indicator is considered a valid indicator of the behaviors it is related or represents.
    valid_from: StixTimestamp
    # The time at which this Indicator should no longer be considered a valid indicator of the behaviors it is
    # related to or represents.
    # If the valid_until property is omitted, then there is no constraint on the latest time for which the
    # Indicator is valid.
    valid_until: StixTimestamp | None = None
    # The kill chain phase(s) to which this Indicator corresponds.
    kill_chain_phases: list[KillChainPhase] | None = None

    @model_validator(mode="after")
    def validate_valid_until_after_valid_from(self) -> Self:
        """
        The valid_until property MUST be greater than the timestamp in the valid_from property.
        """
        if self.valid_from and self.valid_until and self.valid_from > self.valid_until:
            raise ValueError(
                "The valid_until property MUST be greater than the timestamp in the valid_from property"
            )
        return self


# 4.8 Infrastructure
class Infrastructure(StixDomain):
    """
    The Infrastructure SDO represents a type of TTP and describes any systems, software services and any associated
    physical or virtual resources intended to support some purpose (e.g., C2 servers used as part of an attack,
    device or server that are part of defense, database servers targeted by an attack, etc.). While elements of an
    attack can be represented by other SDOs or SCOs, the Infrastructure SDO represents a named group of related data
    that constitutes the infrastructure.
    """

    type: Literal["infrastructure"] = "infrastructure"  # pyright: ignore[reportIncompatibleVariableOverride]
    # A name or characterizing text used to identify the Infrastructure.
    name: str
    # A description that provides more details and context about the Infrastructure,
    # potentially including its purpose, how it is being used, how it relates to other intelligence activities
    # captured in related objects, and its key characteristics.
    description: str | None = None
    # The type of infrastructure being described.
    # The values for this property SHOULD come from the infrastructure-type-ov open vocabulary.
    infrastructure_types: list[str] | None = None
    # Alternative names used to identify this Infrastructure.
    aliases: list[str] | None = None
    # The list of Kill Chain Phases for which this Infrastructure is used.
    kill_chain_phases: list[KillChainPhase] | None = None
    # The time that this Infrastructure was first seen performing malicious activities.
    first_seen: StixTimestamp | None = None
    # The time that this Infrastructure was last seen performing malicious activities.
    last_seen: StixTimestamp | None = None

    @model_validator(mode="after")
    def validate_last_seen_after_first_seen(self) -> Self:
        """
        If the last_seen and the first_seen properties are both defined, then the last_seen property
        MUST be greater than or equal to the timestamp in the first_seen property.
        """
        if self.first_seen and self.last_seen and self.first_seen > self.last_seen:
            raise ValueError(
                "The last_seen property MUST be greater than or equal to the timestamp in the first_seen property"
            )
        return self


# 4.9 Intrusion Set
class IntrusionSet(StixDomain):
    """
    An Intrusion Set is a grouped set of adversarial behaviors and resources with common properties that is believed to
    be orchestrated by a single organization. An Intrusion Set may capture multiple Campaigns or other activities that
    are all tied together by shared attributes indicating a commonly known or unknown Threat Actor. New activity can be
    attributed to an Intrusion Set even if the Threat Actors behind the attack are not known. Threat Actors can move
    from supporting one Intrusion Set to supporting another, or they may support multiple Intrusion Sets.

    Where a Campaign is a set of attacks over a period of time against a specific set of targets to achieve some
    objective, an Intrusion Set is the entire attack package and may be used over a very long period of time in
    multiple Campaigns to achieve potentially multiple purposes.

    While sometimes an Intrusion Set is not active, or changes focus, it is usually difficult to know if it has
    truly disappeared or ended. Analysts may have varying level of fidelity on attributing an Intrusion Set back to
    Threat Actors.
    """

    type: Literal["intrusion-set"] = "intrusion-set"  # pyright: ignore[reportIncompatibleVariableOverride]
    # A name or characterizing text used to identify the Intrusion Set.
    name: str
    # A description that provides more details and context about the Intrusion Set,
    # potentially including its purpose and its key characteristics.
    description: str | None = None
    # Alternative names used to identify this Intrusion Set.
    aliases: list[str] | None = None
    # The time that this Intrusion Set was first seen.
    # A summary property of data from sightings and other data that may or may not be available in STIX.
    # If new sightings are received that are earlier than the first seen timestamp, the object may be updated to
    # account for the new data.
    first_seen: StixTimestamp | None = None
    # The time that this Intrusion Set was last seen.
    # This property is a summary property of data from sightings and other data that may or may not be available.
    # If new sightings are received that are later than the last seen timestamp, the object may be updated to
    # account for the new data.
    last_seen: StixTimestamp | None = None
    # The high-level goals of this Intrusion Set, namely, what are they trying to do.
    # For example, they may be motivated by personal gain, but their goal is to steal credit card numbers.
    # To do this, they may execute specific Campaigns that have detailed objectives like compromising point of sale
    # systems at a large retailer.
    # Another example: to gain information about latest merger and IPO information from ACME Bank.
    goals: list[str] | None = None
    # This property specifies the organizational level at which this Intrusion Set typically works, which in turn
    # determines the resources available to this Intrusion Set for use in an attack.
    # The value for this property SHOULD come from the attack-resource-level-ov open vocabulary.
    resource_level: str | None = None
    # The primary reason, motivation, or purpose behind this Intrusion Set.
    # The value for this property SHOULD come from the attack-motivation-ov open vocabulary.
    primary_motivation: str | None = None
    # The secondary reasons, motivations, or purposes behind this Intrusion Set.
    # The values for this property SHOULD come from the attack-motivation-ov open vocabulary.
    secondary_motivations: list[str] | None = None

    @model_validator(mode="after")
    def validate_last_seen_after_first_seen(self) -> Self:
        """
        If the last_seen and the first_seen properties are both defined, then the last_seen property
        MUST be greater than or equal to the timestamp in the first_seen property.
        """
        if self.first_seen and self.last_seen and self.first_seen > self.last_seen:
            raise ValueError(
                "The last_seen property MUST be greater than or equal to the timestamp in the first_seen property"
            )
        return self


# 4.10 Location
class Location(StixDomain):
    """
    A Location represents a geographic location. The location may be described as any, some or all of the following:
    region (e.g., North America), civic address (e.g. New York, US), latitude and longitude.

    Locations are primarily used to give context to other SDOs. For example, a Location could be used in a
    relationship to describe that the Bourgeois Swallow intrusion set originates from Eastern Europe.

    The Location SDO can be related to an Identity or Intrusion Set to indicate that the identity or intrusion set is
    located in that location. It can also be related from a malware or attack pattern to indicate that they target
    victims in that location. The Location object describes geographic areas, not governments, even in cases where that
    area might have a government. For example, a Location representing the United States describes the United States
    as a geographic area, not the federal government of the United States.
    """

    type: Literal["location"] = "location"  # pyright: ignore[reportIncompatibleVariableOverride]
    # A name used to identify the Location.
    name: str | None = None
    # A textual description of the Location.
    description: str | None = None
    # The latitude of the Location in decimal degrees.
    # Positive numbers describe latitudes north of the equator,
    # and negative numbers describe latitudes south of the equator
    latitude: Annotated[float, Ge(-90.0), Le(90.0)] | None = None
    # The longitude of the Location in decimal degrees.
    # Positive numbers describe longitudes east of the prime meridian
    # and negative numbers describe longitudes west of the prime meridian.
    longitude: Annotated[float, Ge(-180.0), Le(180.0)] | None = None
    # Defines the precision of the coordinates specified by the latitude and longitude properties.
    # This is measured in meters. The actual Location may be anywhere up to precision meters from the defined point.
    precision: float | None = None
    # The region that this Location describes.
    # The value for this property SHOULD come from the region-ov open vocabulary.
    region: str | None = None
    # The country that this Location describes.
    # This property SHOULD contain a valid ISO 3166-1 ALPHA-2 Code [ISO3166-1].
    country: str | None = None
    # The state, province, or other sub-national administrative area that this Location describes.
    # This property SHOULD contain a valid ISO 3166-2 Code [ISO3166-2].
    administrative_area: str | None = None
    # The city that this Location describes.
    city: str | None = None
    # The street address that this Location describes.
    # This property includes all aspects or parts of the street address.
    # For example, some addresses may have multiple lines including a mailstop or apartment number.
    street_address: str | None = None
    # The postal code for the Location.
    postal_code: str | None = None

    @model_validator(mode="after")
    def validate_location_properties(self) -> Self:
        """
        At least one of the following properties/sets of properties MUST be provided:
        - region
        - country
        - latitude and longitude
        """
        if (
            not self.region
            and not self.country
            and not (self.latitude and self.longitude)
        ):
            raise ValueError(
                "At least one of region, country, or both latitude and longitude MUST be provided"
            )

        if self.latitude and not self.longitude:
            raise ValueError("If latitude is present, longitude MUST be present")

        if self.longitude and not self.latitude:
            raise ValueError("If longitude is present, latitude MUST be present")

        if self.precision and (not self.latitude or not self.longitude):
            raise ValueError(
                "If precision is present, latitude and longitude MUST be present"
            )

        return self


# 4.11 Malware
class Malware(StixDomain):
    """
    Malware is a type of TTP that represents malicious code. It generally refers to a program that is inserted into a
    system, usually covertly. The intent is to compromise the confidentiality, integrity, or availability of the
    victim's data, applications, or operating system (OS) or otherwise annoy or disrupt the victim.

    The Malware SDO characterizes, identifies, and categorizes malware instances and families from data that may be
    derived from analysis. This SDO captures detailed information about how the malware works and what it does. This
    SDO captures contextual data relevant to sharing Malware data without requiring the full analysis provided by the
    Malware Analysis SDO.
    """

    type: Literal["malware"] = "malware"  # pyright: ignore[reportIncompatibleVariableOverride]
    # A name used to identify the Malware instance or family, as specified by the producer of the SDO.
    # If a name for a malware instance is not available, the SHA-256 hash value or the filename MAY be used instead.
    name: str | None = None
    # A description that provides more details and context about the Malware instance or family,
    # potentially including its purpose and its key characteristics.
    description: str | None = None
    # A set of categorizations for the malware being described.
    # The values for this property SHOULD come from the malware-type-ov open vocabulary.
    malware_types: list[str] | None = None
    # Whether the object represents a malware family (if true) or a malware instance (if false).
    is_family: bool | None = None
    # Alternative names used to identify this malware or malware family.
    aliases: list[str] | None = None
    # The list of Kill Chain Phases for which this malware can be used.
    kill_chain_phases: list[KillChainPhase] | None = None
    # The time that the malware instance or family was first seen.
    # This property is a summary property of data from sightings and other data that may or may not be available in
    # STIX. If new sightings are received that are earlier than the first seen timestamp,
    # the object may be updated to account for the new data.
    first_seen: StixTimestamp | None = None
    # The time that the malware family or malware instance was last seen.
    # This property is a summary property of data from sightings and other data that may or may not be available in
    # STIX. If new sightings are received that are later than the last_seen timestamp,
    # the object may be updated to account for the new data.
    last_seen: StixTimestamp | None = None
    # The operating systems that the malware family or malware instance is executable on.
    # This applies to virtualized operating systems as well as those running on bare metal.
    operating_system_refs: list[Identifier] | None = None
    # The processor architectures (e.g., x86, ARM, etc.) that the malware instance or family is executable on.
    # The values for this property SHOULD come from the processor-architecture-ov open vocabulary.
    architecture_execution_envs: list[str] | None = None
    # The programming language(s) used to implement the malware instance or family.
    # The values for this property SHOULD come from the implementation-language-ov open vocabulary.
    implementation_languages: list[str] | None = None
    # Any of the capabilities identified for the malware instance or family.
    # The values for this property SHOULD come from the malware-capabilities-ov open vocabulary.
    capabilities: list[str] | None = None
    # The sample_refs property specifies a list of identifiers of the SCO file or artifact objects associated with
    # this malware instance(s) or family.
    sample_refs: list[Identifier] | None = None

    @model_validator(mode="after")
    def validate_last_seen_after_first_seen(self) -> Self:
        """
        If the last_seen and the first_seen properties are both defined, then last_seen property
        MUST be greater than or equal to the timestamp in the first_seen property.
        """
        if self.first_seen and self.last_seen and self.first_seen > self.last_seen:
            raise ValueError(
                "The last_seen property MUST be greater than or equal to the timestamp in the first_seen property"
            )
        return self

    @model_validator(mode="after")
    def validate_name_if_is_family(self) -> Self:
        """
        For a malware family the name MUST be defined.
        """
        if self.is_family and not self.name:
            raise ValueError("For a malware family the name MUST be defined")
        return self


# 4.12 Malware Analysis
class MalwareAnalysis(StixDomain):
    """
    Malware Analysis captures the metadata and results of a particular static or dynamic analysis performed on a malware
    instance or family.
    """

    type: Literal["malware-analysis"] = "malware-analysis"  # pyright: ignore[reportIncompatibleVariableOverride]
    # The name of the analysis engine or product that was used.
    # Product names SHOULD be all lowercase with words separated by a dash "-".
    # For cases where the name of a product cannot be specified, a value of "anonymized" MUST be used.
    product: str
    # The version of the analysis product that was used to perform the analysis.
    version: str | None = None
    # A description of the virtual machine environment used to host the guest operating system (if applicable) that was
    # used for the dynamic analysis of the malware instance or family. If this value is not included in conjunction
    # with the operating_system_ref property, this means that the dynamic analysis may have been performed on bare
    # metal (i.e. without virtualization) or the information was redacted.
    # The value of this property MUST be the identifier for a SCO software object.
    host_vm_ref: Identifier | None = None
    # The operating system used for the dynamic analysis of the malware instance or family. This applies to
    # virtualized operating systems as well as those running on bare metal.
    # The value of this property MUST be the identifier for a SCO software object.
    operating_system_ref: Identifier | None = None
    # Any non-standard software installed on the operating system (specified through the operating-system value)
    # used for the dynamic analysis of the malware instance or family.
    # The value of this property MUST be the identifier for a SCO software object.
    installed_software_refs: list[Identifier] | None = None
    # The named configuration of additional product configuration parameters for this analysis run. For example, when
    # a product is configured to do full depth analysis of Window™ PE files. This configuration may have a named
    # version and that named version can be captured in this property. This will ensure additional runs can be
    # configured in the same way.
    configuration_version: str | None = None
    # The specific analysis modules that were used and configured in the product during this analysis run.
    # For example, configuring a product to support analysis of Dridex.
    modules: list[str] | None = None
    # The version of the analysis engine or product (including AV engines) that was used to perform the analysis.
    analysis_engine_version: str | None = None
    # The version of the analysis definitions used by the analysis tool (including AV tools).
    analysis_definition_version: str | None = None
    # The date and time that the malware was first submitted for scanning or analysis. This value will stay constant
    # while the scanned date can change. For example, when Malware was submitted to a virus analysis tool.
    submitted: StixTimestamp | None = None
    # The date and time that the malware analysis was initiated.
    analysis_started: StixTimestamp | None = None
    # The date and time that the malware analysis ended.
    analysis_ended: StixTimestamp | None = None
    # The classification result or name assigned to the malware instance by the scanner tool.
    result_name: str | None = None
    # The classification result as determined by the scanner or tool analysis process.
    # The value for this property SHOULD come from the malware-result-ov open vocabulary.
    result: str | None = None
    # This property contains the references to the STIX Cyber-observable Objects that were captured during the
    # analysis process.
    analysis_sco_refs: list[Identifier] | None = None
    # This property contains the reference to the SCO file, network traffic or artifact object that this malware
    # analysis was performed against. Caution should be observed when creating an SRO between Malware and Malware
    # Analysis objects when the Malware sample_refs property does not contain the SCO that is included in the
    # Malware Analysis sample_ref property. Note, this property can also contain a reference to an SCO which is not
    # associated with Malware (i.e., some SCO which was scanned and found to be benign.)
    sample_ref: Identifier | None = None

    @model_validator(mode="after")
    def at_least_one_of(self) -> Self:
        """
        One of result or analysis_sco_refs properties MUST be provided.
        """
        if self.result is None and self.analysis_sco_refs is None:
            raise ValueError("One of result or analysis_sco_refs must be provided")
        return self


# 4.13 Note
class Note(StixDomain):
    """
    A Note is intended to convey informative text to provide further context and/or to provide additional analysis
    not contained in the STIX Objects, Marking Definition objects, or Language Content objects which the Note relates
    to. Notes can be created by anyone (not just the original object creator).

    For example, an analyst may add a Note to a Campaign object created by another organization indicating that they've
    seen posts related to that Campaign on a hacker forum.

    Because Notes are typically (though not always) created by human analysts and are comprised of human-oriented text,
    they contain an additional property to capture the analyst(s) that created the Note. This is distinct from the
    created_by_ref property, which is meant to capture the organization that created the object.
    """

    type: Literal["note"] = "note"  # pyright: ignore[reportIncompatibleVariableOverride]
    # A brief summary of the note content.
    abstract: str | None = None
    # The content of the note.
    content: str
    # The name of the author(s) of this note (e.g., the analyst(s) that created it).
    authors: list[str] | None = None
    # The STIX Objects that the note is being applied to.
    object_refs: list[Identifier]


# 4.14 Observed Data
class ObservedData(StixDomain):
    """
    Observed Data conveys information about cyber security related entities such as files, systems, and networks using
    the STIX Cyber-observable Objects (SCOs). For example, Observed Data can capture information about an IP address,
    a network connection, a file, or a registry key. Observed Data is not an intelligence assertion, it is simply the
    raw information without any context for what it means.

    Observed Data can capture that a piece of information was seen one or more times. Meaning, it can capture both a
    single observation of a single entity (file, network connection) as well as the aggregation of multiple
    observations of an entity. When the number_observed property is 1 the Observed Data represents a single entity.
    When the number_observed property is greater than 1, the Observed Data represents several instances of an entity
    potentially collected over a period of time. If a time window is known, that can be captured using the
    first_observed and last_observed properties. When used to collect aggregate data, it is likely that some properties
    in the SCO (e.g., timestamp properties) will be omitted because they would differ for each of the individual
    observations.

    Observed Data may be used by itself (without relationships) to convey raw data collected from any source including
    analyst reports, sandboxes, and network and host-based detection tools. An intelligence producer conveying
    Observed Data SHOULD include as much context (e.g. SCOs) as possible that supports the use of the observed data set
    in systems expecting to utilize the Observed Data for improved security. This includes all SCOs that matched on an
    Indicator pattern and are represented in the collected observed event (or events) being conveyed in the
    Observed Data object. For example, a firewall could emit a single Observed Data instance containing a single
    Network Traffic object for each connection it sees. The firewall could also aggregate data and instead send out an
    Observed Data instance every ten minutes with an IP address and an appropriate number_observed value to indicate
    the number of times that IP address was observed in that window. A sandbox could emit an Observed Data instance
    containing a file hash that it discovered.

    Observed Data may also be related to other SDOs to represent raw data that is relevant to those objects.
    For example, the Sighting Relationship object, can relate an Indicator, Malware, or other SDO to a specific
    Observed Data to represent the raw information that led to the creation of the Sighting (e.g., what was actually
    seen that suggested that a particular instance of malware was active).
    """

    type: Literal["observed-data"] = "observed-data"  # pyright: ignore[reportIncompatibleVariableOverride]
    # The beginning of the time window during which the data was seen.
    first_observed: StixTimestamp
    # The end of the time window during which the data was seen.
    last_observed: StixTimestamp
    # The number of times that each Cyber-observable object represented in the objects or object_refs property was
    # seen. If present, this MUST be an integer between 1 and 999,999,999 inclusive.
    # If the number_observed property is greater than 1, the data contained in the objects or object_refs property was
    # seen multiple times. In these cases, object creators MAY omit properties of the SCO (such as timestamps) that are
    # specific to a single instance of that observed data.
    number_observed: Annotated[int, Ge(1), Le(999999999)]
    # A dictionary of SCO representing the observation. The dictionary MUST contain at least one object.
    # The cyber observable content MAY include multiple objects if those objects are related as part of a single
    # observation. Multiple objects not related to each other via cyber observable Relationships MUST NOT be contained
    # within the same Observed Data instance.
    # For example, a Network Traffic object and two IPv4 Address objects related via the src_ref and dst_ref properties
    # can be contained in the same Observed Data because they are all related and characterize that single entity.
    # NOTE: this property is now deprecated in favor of object_refs and will be removed in a future version.
    objects: Annotated[dict[str, Any], deprecated] | None = None  # pyright: ignore[reportExplicitAny]
    # A list of SCOs and SROs representing the observation. The object_refs MUST contain at least one SCO reference
    # if defined.
    object_refs: list[Identifier] | None = None

    @model_validator(mode="after")
    def validate_last_observed_after_first_observed(self) -> Self:
        """
        The last_observed property MUST be greater than or equal to the timestamp in the first_observed property.
        """
        if (
            self.first_observed
            and self.last_observed
            and self.first_observed > self.last_observed
        ):
            raise ValueError(
                "The last_observed property MUST be greater than or equal to the the first_observed property"
            )
        return self

    @model_validator(mode="after")
    def validate_objects_or_object_refs(self) -> Self:
        """
        The objects property or the object_refs property MUST be provided,
        but both MUST NOT be present at the same time.
        """
        if self.objects is not None and self.object_refs is not None:
            raise ValueError(
                "The objects and object_refs properties MUST NOT be present at the same time"
            )
        if self.objects is None and self.object_refs is None:
            raise ValueError("Either objects or object_refs MUST be provided")
        return self


# 4.15 Opinion
class Opinion(StixDomain):
    """
    An Opinion is an assessment of the correctness of the information in a STIX Object produced by a different entity.
    The primary property is the opinion property, which captures the level of agreement or disagreement using a fixed
    scale. That fixed scale also supports a numeric mapping to allow for consistent statistical operations across
    opinions.

    For example, an analyst from a consuming organization might say that they "strongly disagree" with a Campaign
    object and provide an explanation about why. In a more automated workflow, a SOC operator might give an Indicator
    "one star" in their TIP (expressing "strongly disagree") because it is considered to be a false positive within
    their environment. Opinions are subjective, and the specification does not address how best to interpret them.
    Sharing communities are encouraged to provide clear guidelines to their constituents regarding best practice for
    the use of Opinion objects within the community.

    Because Opinions are typically (though not always) created by human analysts and are comprised of human-oriented
    text, they contain an additional property to capture the analyst(s) that created the Opinion. This is distinct
    from the created_by_ref property, which is meant to capture the organization that created the object.
    """

    type: Literal["opinion"] = "opinion"  # pyright: ignore[reportIncompatibleVariableOverride]
    # An explanation of why the producer has this Opinion. For example, if an Opinion of strongly-disagree is given,
    # the explanation can contain an explanation of why the Opinion producer disagrees and what evidence they have
    # for their disagreement.
    explanation: str | None = None
    # The name of the author(s) of this Opinion (e.g., the analyst(s) that created it).
    authors: list[str] | None = None
    # The opinion that the producer has about all of the STIX Object(s) listed in the object_refs property.
    # The values of this property MUST come from the opinion-enum enumeration.
    opinion: OpinionEnum
    # The STIX Objects that the Opinion is being applied to.
    object_refs: list[Identifier]


# 4.16 Report
class Report(StixDomain):
    """
    Reports are collections of threat intelligence focused on one or more topics, such as a description of a threat
    actor, malware, or attack technique, including context and related details. They are used to group related threat
    intelligence together so that it can be published as a comprehensive cyber threat story.

    The Report SDO contains a list of references to STIX Objects (the CTI objects included in the report) along with a
    textual description and the name of the report.

    For example, a threat report produced by ACME Defense Corp. discussing the Glass Gazelle campaign should be
    represented using Report. The Report itself would contain the narrative of the report while the Campaign SDO and
    any related SDOs (e.g., Indicators for the Campaign, Malware it uses, and the associated Relationships) would be
    referenced in the report contents.
    """

    type: Literal["report"] = "report"  # pyright: ignore[reportIncompatibleVariableOverride]
    # A name or characterizing text used to identify the Report.
    name: str
    # A description that provides more details and context about the Report, potentially including its purpose and
    # its key characteristics.
    description: str | None = None
    # The primary type(s) of content found in this report.
    # The values for this property SHOULD come from the report-type-ov open vocabulary.
    report_types: list[str] | None = None
    # The date that this Report object was officially published by the creator of this report.
    # The publication date (public release, legal release, etc.) may be different than the date the report was
    # created or shared internally (the date in the created property).
    published: StixTimestamp
    # Specifies the STIX Objects that are referred to by this Report.
    object_refs: list[Identifier]


# 4.17 Threat Actor
class ThreatActor(StixDomain):
    """
    Threat Actors are actual individuals, groups, or organizations believed to be operating with malicious intent.
    A Threat Actor is not an Intrusion Set but may support or be affiliated with various Intrusion Sets, groups, or
    organizations over time.

    Threat Actors leverage their resources, and possibly the resources of an Intrusion Set, to conduct attacks and
    run Campaigns against targets.

    Threat Actors can be characterized by their motives, capabilities, goals, sophistication level, past activities,
    resources they have access to, and their role in the organization.
    """

    type: Literal["threat-actor"] = "threat-actor"  # pyright: ignore[reportIncompatibleVariableOverride]
    # A name or characterizing text used to identify the Threat Actor or Threat Actor group.
    name: str
    # A description that provides more details and context about the Threat Actor, potentially including its purpose
    # and its key characteristics.
    description: str | None = None
    # The type(s) of this threat actor.
    # The values for this property SHOULD come from the threat-actor-type-ov open vocabulary.
    threat_actor_types: list[str] | None = None
    # A list of other names that this Threat Actor is believed to use.
    aliases: list[str] | None = None
    # The time that this Threat Actor was first seen.
    # This property is a summary property of data from sightings and other data that may or may not be available in
    # STIX. If new sightings are received that are earlier than the first seen timestamp, the object may be updated
    # to account for the new data.
    first_seen: StixTimestamp | None = None
    # The time that this Threat Actor was last seen.
    # This property is a summary property of data from sightings and other data that may or may not be available in
    # STIX. If new sightings are received that are later than the last seen timestamp, the object may be updated to
    # account for the new data
    last_seen: StixTimestamp | None = None
    # A list of roles the Threat Actor plays.
    # The values for this property SHOULD come from the threat-actor-role-ov open vocabulary.
    roles: list[str] | None = None
    # The high-level goals of this Threat Actor, namely, *what* are they trying to do.
    # For example, they may be motivated by personal gain, but their goal is to steal credit card numbers.
    # To do this, they may execute specific Campaigns that have detailed objectives like compromising point of sale
    # systems at a large retailer.
    goals: list[str] | None = None
    # The skill, specific knowledge, special training, or expertise a Threat Actor must have to perform the attack.
    # The value for this property SHOULD come from the threat-actor-sophistication-ov open vocabulary.
    sophistication: str | None = None
    # The organizational level at which this Threat Actor typically works, which in turn determines the resources
    # available to this Threat Actor for use in an attack.
    # This attribute is linked to the sophistication property — a specific resource level implies that the
    # Threat Actor has access to at least a specific sophistication level.
    # The value for this property SHOULD come from the attack-resource-level-ov open vocabulary.
    resource_level: str | None = None
    # The primary reason, motivation, or purpose behind this Threat Actor.
    # The motivation is *why* the Threat Actor wishes to achieve the goal (what they are trying to achieve).
    # The value for this property SHOULD come from the attack-motivation-ov open vocabulary.
    primary_motivation: str | None = None
    # This property specifies the secondary reasons, motivations, or purposes behind this Threat Actor.
    # These motivations can exist as an equal or near-equal cause to the primary motivation. However, it does not
    # replace or necessarily magnify the primary motivation, but it might indicate additional context.
    # The position in the list has no significance.
    # The value for this property SHOULD come from the attack-motivation-ov open vocabulary.
    secondary_motivations: list[str] | None = None
    # The personal reasons, motivations, or purposes of the Threat Actor regardless of organizational goals.
    # Personal motivation, which is independent of the organization's goals, describes what impels an individual to
    # carry out an attack. Personal motivation may align with the organization's motivation
    # — as is common with activists — but more often it supports personal goals. For example, an individual analyst may
    # join a Data Miner corporation because his or her skills may align with the corporation's objectives.
    # But the analyst most likely performs his or her daily work toward those objectives for personal reward in the
    # form of a paycheck. The motivation of personal reward may be even stronger for Threat Actors who commit illegal
    # acts, as it is more difficult for someone to cross that line purely for altruistic reasons.
    # The values for this property SHOULD come from the attack-motivation-ov open vocabulary.
    # The position in the list has no significance.
    personal_motivations: list[str] | None = None

    @model_validator(mode="after")
    def validate_last_seen_after_first_seen(self) -> Self:
        """
        If the last_seen property and the first_seen property are both defined, then the last_seen property
        MUST be greater than or equal to the timestamp in the first_seen property.
        """
        if self.first_seen and self.last_seen and self.first_seen > self.last_seen:
            raise ValueError(
                "The last_seen property MUST be greater than or equal to the timestamp in the first_seen property"
            )
        return self


# 4.18 Tool
class Tool(StixDomain):
    """
    Tools are legitimate software that can be used by threat actors to perform attacks. Knowing how and when threat
    actors use such tools can be important for understanding how campaigns are executed. Unlike malware, these tools
    or software packages are often found on a system and have legitimate purposes for power users, system
    administrators, network administrators, or even normal users. Remote access tools (e.g., RDP) and network
    scanning tools (e.g., Nmap) are examples of Tools that may be used by a Threat Actor during an attack.

    The Tool SDO characterizes the properties of these software tools and can be used as a basis for making an
    assertion about how a Threat Actor uses them during an attack. It contains properties to name and describe the
    tool, a list of Kill Chain Phases the tool can be used to carry out, and the version of the tool.

    This SDO MUST NOT be used to characterize malware. Further, Tool MUST NOT be used to characterize tools used as
    part of a course of action in response to an attack.
    """

    type: Literal["tool"] = "tool"  # pyright: ignore[reportIncompatibleVariableOverride]
    # A name or characterizing text used to identify the Tool.
    name: str
    # A description that provides more details and context about the Tool, potentially including its purpose and
    # its key characteristics.
    description: str | None = None
    # The kind(s) of tool(s) being described.
    # The values for this property SHOULD come from the tool-type-ov open vocabulary.
    tool_types: list[str] | None = None
    # Alternative names used to identify this Tool.
    aliases: list[str] | None = None
    # The list of kill chain phases for which this Tool can be used.
    kill_chain_phases: list[KillChainPhase] | None = None
    # The version identifier associated with the Tool.
    tool_version: str | None = None


# 4.19 Vulnerability
class Vulnerability(StixDomain):
    """
    A Vulnerability is a weakness or defect in the requirements, designs, or implementations of the computational
    logic (e.g., code) found in software and some hardware components (e.g., firmware) that can be directly
    exploited to negatively impact the confidentiality, integrity, or availability of that system.

    CVE is a list of information security vulnerabilities and exposures that provides common names for publicly known
    problems [CVE]. For example, if a piece of malware exploits CVE-2015-12345, a Malware object could be linked to a
    Vulnerability object that references CVE-2015-12345.

    The Vulnerability SDO is primarily used to link to external definitions of vulnerabilities or to describe 0-day
    vulnerabilities that do not yet have an external definition. Typically, other SDOs assert relationships to
    Vulnerability objects when a specific vulnerability is targeted and exploited as part of malicious cyber activity.
    As such, Vulnerability objects can be used as a linkage to the asset management and compliance process.
    """

    type: Literal["vulnerability"] = "vulnerability"  # pyright: ignore[reportIncompatibleVariableOverride]
    # A list of external references which refer to non-STIX information.
    # This property MAY be used to provide one or more Vulnerability identifiers, such as a CVE ID [CVE].
    # When specifying a CVE ID, the source_name property of the external reference MUST be set to cve and the
    # external_id property MUST be the exact CVE identifier.
    external_references: list[ExternalReference] | None = None
    # A name or characterizing text used to identify the Vulnerability.
    name: str
    # A description that provides more details and context about the Vulnerability, potentially including its
    # purpose and its key characteristics.
    description: str | None = None


SDOs = Annotated[
    (
        AttackPattern
        | Campaign
        | CourseOfAction
        | Grouping
        | Identity
        | Incident
        | Indicator
        | Infrastructure
        | IntrusionSet
        | Location
        | Malware
        | MalwareAnalysis
        | Note
        | ObservedData
        | Opinion
        | Report
        | ThreatActor
        | Tool
        | Vulnerability
    ),
    Field(discriminator="type"),
]
