from typing import Literal, Annotated, Self
from datetime import datetime
from pydantic import Field
from pydantic.functional_validators import model_validator
from stidantic.types import StixDomain, KillChainPhase


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
    first_seen: datetime | None = None
    # The time that this Campaign was last seen.
    # A summary property of data from sightings and other data that may or may not be available in STIX.
    # If new sightings are received that are later than the last seen timestamp,
    # the object may be updated to account for the new data.
    last_seen: datetime | None = None
    # The Campaign’s primary goal, objective, desired outcome, or intended effect
    # — what the Threat Actor or Intrusion Set hopes to accomplish with this Campaign.
    objective: str | None = None

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


SDOs = Annotated[(AttackPattern | Campaign), Field(discriminator="type")]
