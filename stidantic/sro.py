from typing import Literal, Self, Annotated
from datetime import datetime
from pydantic import Field
from pydantic.functional_validators import model_validator
from pydantic.types import PositiveInt
from stidantic.types import StixRelationship, Identifier, StixType


# 5.1 Relationship
class Relationship(StixRelationship):
    """
    The Relationship object is used to link together two SDOs or SCOs in order to describe how they are related to
    each other. If SDOs and SCOs are considered "nodes" or "vertices" in the graph, the Relationship Objects (SROs)
    represent "edges".

    STIX defines many relationship types to link together SDOs and SCOs. These relationships are contained in the
    "Relationships" table under each SDO and SCO definition. Relationship types defined in the specification SHOULD
    be used to ensure consistency. An example of a specification-defined relationship is that an indicator indicates
    a campaign. That relationship type is listed in the Relationships section of the Indicator SDO definition.

    STIX also allows relationships from any SDO or SCO to any SDO or SCO that have not been defined in this
    specification. These relationships MAY use the related-to relationship type or MAY use a user-defined
    relationship type. As an example, a user might want to link malware directly to a tool.
    They can do so using related-to to say that the Malware is related to the Tool but not describe how,
    or they could use delivered-by (a user-defined name they determined) to indicate more detail.

    Note that some relationships in STIX may seem like "shortcuts". For example, an Indicator doesn't really detect
    a Campaign: it detects activity (Attack Patterns, Malware, Infrastructure, etc.) that are often used by that
    campaign. While some analysts might want all of the source data and think that shortcuts are misleading,
    in many cases it's helpful to provide just the key points (shortcuts) and leave out the low-level details.
    In other cases, the low-level analysis may not be known or sharable, while the high-level analysis is.
    For these reasons, relationships that might appear to be "shortcuts" are not excluded from STIX.
    """

    type: Literal["relationship"] = "relationship"  # pyright: ignore[reportIncompatibleVariableOverride]
    # The name used to identify the type of Relationship. This value SHOULD be an exact value listed in the
    # relationships for the source and target SDO, but MAY be any string.
    relationship_type: StixType
    # A description that provides more details and context about the Relationship,
    # potentially including its purpose and its key characteristics.
    description: str | None = None
    # The id of the source (from) object. The value MUST be an ID reference to an SDO or SCO
    # (i.e., it cannot point to an SRO, Bundle, Language Content, or Marking Definition).
    source_ref: Identifier
    # The id of the target (to) object. The value MUST be an ID reference to an SDO or SCO
    # (i.e., it cannot point to an SRO, Bundle, Language Content, or Marking Definition).
    target_ref: Identifier
    # This optional timestamp represents the earliest time at which the Relationship between the objects exists.
    # If this property is a future timestamp, at the time the start_time property is defined,
    # then this represents an estimate by the producer of the intelligence of the earliest
    # time at which relationship will be asserted to be true.
    # If it is not specified, then the earliest time at which the relationship between the objects exists
    # is not defined.
    start_time: datetime | None = None
    # The latest time at which the Relationship between the objects exists. If this property is a future timestamp,
    # at the time the stop_time property is defined, then this represents an estimate by the producer of the
    # intelligence of the latest time at which relationship will be asserted to be true.
    # If stop_time is not specified, then the latest time at which the relationship between
    # the objects exists is either not known, not disclosed, or has no defined stop time.
    stop_time: datetime | None = None

    @model_validator(mode="after")
    def validate_start_stop_interval(self) -> Self:
        """
        If start_time and stop_time are both defined, then stop_time MUST be later than the start_time value.
        """
        if self.start_time and self.stop_time and self.start_time > self.stop_time:
            raise ValueError(
                "the stop_time property MUST be greater than or equal to the timestamp in the start_time property"
            )
        return self


# 5.2 Sighting
class Sighting(StixRelationship):
    """
    A Sighting denotes the belief that something in CTI (e.g., an indicator, malware, tool, threat actor, etc.)
    was seen. Sightings are used to track who and what are being targeted, how attacks are carried out, and to
    track trends in attack behavior.

    The Sighting relationship object is a special type of SRO; it is a relationship that contains extra properties
    not present on the Generic Relationship object. These extra properties are included to represent data specific
    to sighting relationships (e.g., count, representing how many times something was seen), but for other purposes
    a Sighting can be thought of as a Relationship with a name of "sighting-of". Sighting is captured as a relationship
    because you cannot have a sighting unless you have something that has been sighted.
    Sighting does not make sense without the relationship to what was sighted.

    Sighting relationships relate three aspects of the sighting:
    ●      What was sighted, such as the Indicator, Malware, Campaign, or other SDO (sighting_of_ref)
    ●      Who sighted it and/or where it was sighted, represented as an Identity (where_sighted_refs)
    ●      What was actually seen on systems and networks, represented as Observed Data (observed_data_refs)

    What was sighted is required; a sighting does not make sense unless you say what you saw. Who sighted it,
    where it was sighted, and what was actually seen are optional. In many cases it is not necessary to provide
    that level of detail in order to provide value.

    Sightings are used whenever any SDO has been "seen". In some cases, the object creator wishes to convey very little
    information about the sighting; the details might be sensitive, but the fact that they saw a malware instance or
    threat actor could still be very useful. In other cases, providing the details may be helpful or even necessary;
    saying exactly which of the 1000 IP addresses in an indicator were sighted is helpful when tracking which of those
    IPs is still malicious.

    Sighting is distinct from Observed Data in that Sighting is an intelligence assertion ("I saw this threat actor")
    while Observed Data is simply information ("I saw this file"). When you combine them by including the linked
    Observed Data (observed_data_refs) from a Sighting, you can say "I saw this file, and that makes me think I saw
    this threat actor".
    """

    type: Literal["sighting"] = "sighting"  # pyright: ignore[reportIncompatibleVariableOverride]
    # A description that provides more details and context about the Sighting.
    description: str | None = None
    # The beginning of the time window during which the SDO referenced by the sighting_of_ref property was sighted.
    first_seen: datetime | None = None
    # The end of the time window during which the SDO referenced by the sighting_of_ref property was sighted.
    last_seen: datetime | None = None
    # If present, this MUST be an integer between 0 and 999,999,999 inclusive and represents the number of times the
    # SDO referenced by the sighting_of_ref property was sighted.
    # Observed Data has a similar property called number_observed, which refers to the number of times the data was
    # observed. These counts refer to different concepts and are distinct.
    # For example, a single sighting of a DDoS bot might have many millions of observations of the network traffic
    # that it generates. Thus, the Sighting count would be 1 (the bot was observed once) but the Observed Data
    # number_observed would be much higher.
    # As another example, a sighting with a count of 0 can be used to express that an indicator was not seen at all.
    count: PositiveInt | None = None
    # An ID reference to the SDO that was sighted (e.g., Indicator or Malware).
    # For example, if this is a Sighting of an Indicator, that Indicator’s ID would be the value of this property.
    # This property MUST reference only an SDO.
    sighting_of_ref: Identifier | None = None
    # A list of ID references to the Observed Data objects that contain the raw cyber data for this Sighting.
    # For example, a Sighting of an Indicator with an IP address could include the Observed Data for the
    # network connection that the Indicator was used to detect.
    # This property MUST reference only Observed Data SDOs.
    observed_data_refs: list[Identifier] | None = None
    # A list of ID references to the Identity or Location objects describing the entities or types of entities
    # that saw the sighting.
    # Omitting the where_sighted_refs property does not imply that the sighting was seen by the object creator.
    # To indicate that the sighting was seen by the object creator, an Identity representing the object creator
    # should be listed in where_sighted_refs.
    # This property MUST reference only Identity or Location SDOs.
    where_sighted_refs: list[Identifier] | None = None
    # The summary property indicates whether the Sighting should be considered summary data.
    # Summary data is an aggregation of previous Sightings reports and should not be considered primary source data.
    # Default value is false.
    summary: bool | None = False

    @model_validator(mode="after")
    def validate_first_last_interval(self) -> Self:
        """
        If this property and the first_seen property are both defined, then this property
        MUST be greater than or equal to the timestamp in the first_seen property.
        """
        if self.first_seen and self.last_seen and self.first_seen > self.last_seen:
            raise ValueError(
                "the last_seen property MUST be greater than or equal to the timestamp in the first_seen property"
            )
        return self


SROs = Annotated[(Relationship | Sighting), Field(discriminator="type")]
