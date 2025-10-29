from enum import Enum


class AccountType(Enum):
    facebook = "facebook"
    ldap = "ldap"
    nis = "nis"
    openid = "openid"
    radius = "radius"
    skype = "skype"
    tacacs = "tacacs"
    twitter = "twitter"
    unix = "unix"
    windows_local = "windows-local"
    windows_domain = "windows-domain"


class AttackMotivation(Enum):
    accidental = "accidental"
    coercion = "coercion"
    dominance = "dominance"
    ideology = "ideology"
    notoriety = "notoriety"
    organizational_gain = "organizational-gain"
    personal_gain = "personal-gain"
    personal_satisfaction = "personal-satisfaction"
    revenge = "revenge"
    unpredictable = "unpredictable"


class AttackResourceLevel(Enum):
    individual = "individual"
    club = "club"
    contest = "contest"
    team = "team"
    organization = "organization"
    government = "government"


class EncryptionAlgorithm(Enum):
    aes_256_gcm = "AES-256-GCM"
    chacha20_poly1305 = "ChaCha20-Poly1305"
    mime_type_indicated = "mime-type-indicated"


class ExtensionType(Enum):
    new_sdo = "new-sdo"
    new_sco = "new-sco"
    new_sro = "new-sro"
    property_extension = "property-extension"
    toplevel_property_extension = "toplevel-property-extension"


class GroupingContext(Enum):
    suspicious_activity = "suspicious-activity"
    malware_analysis = "malware-analysis"
    unspecified = "unspecified"


class HashingAlgorithm(Enum):
    md5 = "MD5"
    sha1 = "SHA-1"
    sha_256 = "SHA-256"
    sha_512 = "SHA-512"
    sha3_256 = "SHA3-256"
    sha3_512 = "SHA3-512"
    ssdeep = "SSDEEP"
    tlsh = "TLSH"


class IdentityClass(Enum):
    individual = "individual"
    group = "group"
    system = "system"
    organization = "organization"
    class_ = "class"
    unknown = "unknown"


class ImplementationLanguage(Enum):
    applescript = "applescript"
    bash = "bash"
    c = "c"
    cpp = "c++"
    csharp = "c#"
    go = "go"
    java = "java"
    javascript = "javascript"
    lua = "lua"
    objective_c = "objective-c"
    perl = "perl"
    php = "php"
    powershell = "powershell"
    python = "python"
    ruby = "ruby"
    scala = "scala"
    swift = "swift"
    typescript = "typescript"
    visual_basic = "visual-basic"
    x86_32 = "x86-32"
    x86_64 = "x86-64"


class IndicatorType(Enum):
    anomalous_activity = "anomalous-activity"
    anonymization = "anonymization"
    benign = "benign"
    compromised = "compromised"
    malicious_activity = "malicious-activity"
    attribution = "attribution"
    unknown = "unknown"


class IndustrySector(Enum):
    agriculture = "agriculture"
    aerospace = "aerospace"
    automotive = "automotive"
    chemical = "chemical"
    commercial = "commercial"
    communications = "communications"
    construction = "construction"
    defense = "defense"
    education = "education"
    energy = "energy"
    entertainment = "entertainment"
    financial_services = "financial-services"
    government = "government "
    emergency_services = "emergency-services"
    government_local = "government-local"
    government_national = "government-national"
    government_public_services = "government-public-services"
    government_regional = "government-regional"
    healthcare = "healthcare"
    hospitality_leisure = "hospitality-leisure"
    infrastructure = "infrastructure"
    dams = "dams"
    nuclear = "nuclear"
    water = "water"
    insurance = "insurance"
    manufacturing = "manufacturing"
    mining = "mining"
    non_profit = "non-profit"
    pharmaceuticals = "pharmaceuticals"
    retail = "retail"
    technology = "technology"
    telecommunications = "telecommunications"
    transportation = "transportation"
    utilities = "utilities"


class InfrastructureType(Enum):
    amplification = "amplification"
    anonymization = "anonymization"
    botnet = "botnet"
    command_and_control = "command-and-control"
    exfiltration = "exfiltration"
    hosting_malware = "hosting-malware"
    hosting_target_lists = "hosting-target-lists"
    phishing = "phishing"
    reconnaissance = "reconnaissance"
    staging = "staging"
    unknown = "unknown"


class MalwareResult(Enum):
    malicious = "malicious"
    suspicious = "suspicious"
    benign = "benign"
    unknown = "unknown"


class MalwareCapabilities(Enum):
    accesses_remote_machines = "accesses-remote-machines"
    anti_debugging = "anti-debugging"
    anti_disassembly = "anti-disassembly"
    anti_emulation = "anti-emulation"
    anti_memory_forensics = "anti-memory-forensics"
    anti_sandbox = "anti-sandbox"
    anti_vm = "anti-vm"
    captures_input_peripherals = "captures-input-peripherals"
    captures_output_peripherals = "captures-output-peripherals"
    captures_system_state_data = "captures-system-state-data"
    cleans_traces_of_infection = "cleans-traces-of-infection"
    commits_fraud = "commits-fraud"
    communicates_with_c2 = "communicates-with-c2"
    compromises_data_availability = "compromises-data-availability"
    compromises_data_integrity = "compromises-data-integrity"
    compromises_system_availability = "compromises-system-availability"
    controls_local_machine = "controls-local-machine"
    degrades_security_software = "degrades-security-software"
    degrades_system_updates = "degrades-system-updates"
    determines_c2_server = "determines-c2-server"
    emails_spam = "emails-spam"
    escalates_privileges = "escalates-privileges"
    evades_av = "evades-av"
    exfiltrates_data = "exfiltrates-data"
    fingerprints_host = "fingerprints-host"
    hides_artifacts = "hides-artifacts"
    hides_executing_code = "hides-executing-code"
    infects_files = "infects-files"
    infects_remote_machines = "infects-remote-machines"
    installs_other_components = "installs-other-components"
    persists_after_system_reboot = "persists-after-system-reboot"
    prevents_artifact_access = "prevents-artifact-access"
    prevents_artifact_deletion = "prevents-artifact-deletion"
    probes_network_environment = "probes-network-environment"
    self_modifies = "self-modifies"
    steals_authentication_credentials = "steals-authentication-credentials"
    violates_system_operational_integrity = "violates-system-operational-integrity"


class MalwareType(Enum):
    adware = "adware"
    backdoor = "backdoor"
    bot = "bot"
    bootkit = "bootkit"
    ddos = "ddos"
    downloader = "downloader"
    dropper = "dropper"
    exploit_kit = "exploit-kit"
    keylogger = "keylogger"
    ransomware = "ransomware"
    remote_access_trojan = "remote-access-trojan"
    resource_exploitation = "resource-exploitation"
    rogue_security_software = "rogue-security-software"
    rootkit = "rootkit"
    screen_capture = "screen-capture"
    spyware = "spyware"
    trojan = "trojan"
    unknown = "unknown"
    virus = "virus"
    webshell = "webshell"
    wiper = "wiper"
    worm = "worm"


class NetworkSocketAddressFamily(Enum):
    UNSPEC = "AF_UNSPEC"
    INET = "AF_INET"
    IPX = "AF_IPX"
    APPLETALK = "AF_APPLETALK"
    NETBIOS = "AF_NETBIOS"
    INET6 = "AF_INET6"
    IRDA = "AF_IRDA"
    BTH = "AF_BTH"


class NetworkSocketType(Enum):
    SOCK_STREAM = "SOCK_STREAM"
    AF_ISOCK_DGRAMNET = "AF_ISOCK_DGRAMNET"
    SOCK_RAW = "SOCK_RAW"
    SOCK_RDM = "SOCK_RDM"
    SOCK_SEQPACKET = "SOCK_SEQPACKET"


class OpinionEnum(Enum):
    strongly_disagree = "strongly-disagree"
    disagree = "disagree"
    neutral = "neutral"
    agree = "agree"
    strongly_agree = "strongly-agree"


class PatternType(Enum):
    stix = "stix"
    pcre = "pcre"
    sigma = "sigma"
    snort = "snort"
    suricata = "suricata"
    yara = "yara"


class ProcessorArchitecture(Enum):
    alpha = "alpha"
    arm = "arm"
    ia_64 = "ia-64"
    mips = "mips"
    powerpc = "powerpc"
    sparc = "sparc"
    x86 = "x86"
    x86_64 = "x86-64"


class Region(Enum):
    africa = "africa"
    eastern_africa = "eastern-africa"
    middle_africa = "middle-africa"
    northern_africa = "northern-africa"
    southern_africa = "southern-africa"
    western_africa = "western-africa"
    americas = "americas"
    caribbean = "caribbean"
    central_america = "central-america"
    latin_america_caribbean = "latin-america-caribbean"
    northern_america = "northern-america"
    south_america = "south-america"
    asia = "asia"
    central_asia = "central-asia"
    eastern_asia = "eastern-asia"
    southern_asia = "southern-asia"
    south_eastern_asia = "south-eastern-asia"
    western_asia = "western-asia"
    europe = "europe"
    eastern_europe = "eastern-europe"
    northern_europe = "northern-europe"
    southern_europe = "southern-europe"
    western_europe = "western-europe"
    oceania = "oceania"
    antarctica = "antarctica"
    australia_new_zealand = "australia-new-zealand"
    melanesia = "melanesia"
    micronesia = "micronesia"
    polynesia = "polynesia"


class ReportType(Enum):
    attack_pattern = "attack-pattern"
    campaign = "campaign"
    identity = "identity"
    indicator = "indicator"
    intrusion_set = "intrusion-set"
    malware = "malware"
    observed_data = "observed-data"
    threat_actor = "threat-actor"
    threat_report = "threat-report"
    tool = "tool"
    vulnerability = "vulnerability"


class ThreatActorType(Enum):
    activist = "activist"
    competitor = "competitor"
    crime_syndicate = "crime-syndicate"
    criminal = "criminal"
    hacker = "hacker"
    insider_accidental = "insider-accidental"
    insider_disgruntled = "insider-disgruntled"
    nation_state = "nation-state"
    sensationalist = "sensationalist"
    spy = "spy"
    terrorist = "terrorist"
    unknown = "unknown"


class ThreatActorRole(Enum):
    agent = "agent"
    director = "director"
    independent = "independent"
    infrastructure_architect = "infrastructure-architect"
    infrastructure_operator = "infrastructure-operator"
    malware_author = "malware-author"
    sponsor = "sponsor"


class ThreatActorSophistication(Enum):
    none = "none"
    minimal = "minimal"
    intermediate = "intermediate"
    advanced = "advanced"
    expert = "expert"
    innovator = "innovator"
    strategic = "strategic"


class ToolType(Enum):
    denial_of_service = "denial-of-service"
    exploitation = "exploitation"
    information_gathering = "information-gathering"
    network_capture = "network-capture"
    credential_exploitation = "credential-exploitation"
    remote_access = "remote-access"
    vulnerability_scanning = "vulnerability-scanning"
    unknown = "unknown"


class WindowsIntegrityLevel(Enum):
    low = "low"
    medium = "medium"
    high = "high"
    system = "system"


class WindowsPEBinary(Enum):
    dll = "dll"
    exe = "exe"
    sys = "sys"


class WindowsRegistryDatatype(Enum):
    NONE = "REG_NONE"
    SZ = "REG_SZ"
    EXPAND_SZ = "REG_EXPAND_SZ"
    BINARY = "REG_BINARY"
    DWORD = "REG_DWORD"
    DWORD_BIG_ENDIAN = "REG_DWORD_BIG_ENDIAN"
    DWORD_LITTLE_ENDIAN = "REG_DWORD_LITTLE_ENDIAN"
    LINK = "REG_LINK"
    MULTI_SZ = "REG_MULTI_SZ"
    RESOURCE_LIST = "REG_RESOURCE_LIST"
    FULL_RESOURCE_DESCRIPTION = "REG_FULL_RESOURCE_DESCRIPTION"
    RESOURCE_REQUIREMENTS_LIST = "REG_RESOURCE_REQUIREMENTS_LIST"
    QWORD = "REG_QWORD"
    INVALID_TYPE = "REG_INVALID_TYPE"


class WindowsServiceStartType(Enum):
    AUTO_START = "SERVICE_AUTO_START"
    BOOT_START = "SERVICE_BOOT_START"
    DEMAND_START = "SERVICE_DEMAND_START"
    DISABLED = "SERVICE_DISABLED"
    SYSTEM_ALERT = "SERVICE_SYSTEM_ALERT"


class WindowsServiceType(Enum):
    KERNEL_DRIVER = "SERVICE_KERNEL_DRIVER"
    FILE_SYSTEM_DRIVER = "SERVICE_FILE_SYSTEM_DRIVER"
    WIN32_OWN_PROCESS = "SERVICE_WIN32_OWN_PROCESS"
    WIN32_SHARE_PROCESS = "SERVICE_WIN32_SHARE_PROCESS"


class WindowsServiceStatus(Enum):
    CONTINUE_PENDING = "SERVICE_CONTINUE_PENDING"
    PAUSE_PENDING = "SERVICE_PAUSE_PENDING"
    PAUSED = "SERVICE_PAUSED"
    RUNNING = "SERVICE_RUNNING"
    START_PENDING = "SERVICE_START_PENDING"
    STOP_PENDING = "SERVICE_STOP_PENDING"
    STOPPED = "SERVICE_STOPPED"


class DNSRecord(Enum):
    A = "A"  # Address record : Returns a 32-bit IPv4 address, most commonly used to map hostnames to an IP address
    # of the host, but it is also used for DNSBLs, storing subnet masks in RFC 1101, etc.
    AAAA = "AAAA"  # IPv6 address record : Returns a 128-bit IPv6 address, most commonly used to map hostnames
    # to an IP address of the host.
    AFSDB = "AFSDB"  # AFS database record : Location of database servers of an AFS cell. This record is commonly
    # used by AFS clients to contact AFS cells outside their local domain.
    APL = "APL"  # Address Prefix List : Specify lists of address ranges, e.g. in CIDR format,
    # for various address families. Experimental.
    CAA = "CAA"  # Certification Authority Authorization : DNS Certification Authority Authorization,
    # constraining acceptable CAs for a host/domain
    CDNSKEY = "CDNSKEY"  # Child copy of DNSKEY record, for transfer to parent
    CDS = "CDS"  # Child DS : Child copy of DS record, for transfer to parent
    CERT = "CERT"  # Certificate record : Stores PKIX, SPKI, PGP, etc.
    CNAME = "CNAME"  # Canonical name record : Alias of one name to another: the DNS lookup will continue
    # by retrying the lookup with the new name.
    CSYNC = "CSYNC"  # Child-to-Parent Synchronization : Specify a synchronization mechanism between a child
    # and a parent DNS zone. Typical example is declaring the same NS records in the parent and the child zone
    DHCID = (
        "DHCID"  # DHCP identifier : Used in conjunction with the FQDN option to DHCP
    )
    DLV = "DLV"  # DNSSEC Lookaside Validation record : For publishing DNSSEC trust anchors outside of the
    # DNS delegation chain. Uses the same format as the DS record. RFC 5074 describes a way of using these records.
    DNAME = "DNAME"  # Delegation name record : Alias for a name and all its subnames, unlike CNAME, which is an alias
    # for only the exact name. Like a CNAME, the DNS lookup will continue by retrying the lookup with the new name.
    DNSKEY = "DNSKEY"  # DNS Key record : The key record used in DNSSEC. Uses the same format as the KEY record.
    DS = "DS"  # Delegation signer : The record used to identify the DNSSEC signing key of a delegated zone
    EUI48 = "EUI48"  # MAC address (EUI-48) : A 48-bit IEEE Extended Unique Identifier.
    EUI64 = "EUI64"  # MAC address (EUI-64) : A 64-bit IEEE Extended Unique Identifier.
    HINFO = "HINFO"  # Host Information : Providing Minimal-Sized Responses to DNS Queries That Have QTYPE=ANY
    HIP = "HIP"  # Host Identity Protocol : Method of separating the end-point identifier and locator roles of IPs.
    HTTPS = "HTTPS"  # HTTPS Binding : RR that improves performance for clients that need to resolve many resources
    # to access a domain. More info in this IETF Draft by DNSOP Working group and Akamai technologies.
    IPSECKEY = "IPSECKEY"  # IPsec Key : Key record that can be used with IPsec
    KEY = "KEY"  # Key record
    KX = "KX"  # Key Exchanger record : Used with some cryptographic systems (not including DNSSEC) to identify
    # a key management agent for the associated domain-name. Note that this has nothing to do with DNS Security.
    LOC = "LOC"  # Location record : Specifies a geographical location associated with a domain name
    MX = "MX"  # Mail exchange record : List of mail exchange servers that accept email for a domain
    NAPTR = "NAPTR"  # Naming Authority Pointer : Allows regular-expression-based rewriting of domain names
    # which can then be used as URIs, further domain names to lookups, etc.
    NS = "NS"  # Name server record : Delegates a DNS zone to use the given authoritative name servers
    NSEC = "NSEC"  # Next Secure record : Part of DNSSEC—used to prove a name does not exist.
    NSEC3 = "NSEC3"  # Next Secure record version 3 : An extension to DNSSEC that allows proof of nonexistence
    # for a name without permitting zonewalking
    NSEC3PARAM = "NSEC3PARAM"  # NSEC3 parameters : Parameter record for use with NSEC3
    OPENPGPKEY = "OPENPGPKEY"  # OpenPGP public key record : A DNS-based Authentication of Named Entities (DANE) method
    # for publishing and locating OpenPGP public keys in DNS for a specific email address.
    PTR = "PTR"  # PTR Resource Record [de] : Pointer to a canonical name. Unlike a CNAME, DNS processing stops and
    # just the name is returned. The most common use is for implementing reverse DNS lookups.
    RRSIG = "RRSIG"  # DNSSEC signature : Signature for a DNSSEC-secured record set. Same format as the SIG record.
    RP = "RP"  # Responsible Person : Information about the responsible person(s) for the domain.
    # Usually an email address with the @ replaced by a .
    SIG = "SIG"  # Signature
    SMIMEA = "SMIMEA"  # S/MIME cert association : Associates an S/MIME certificate with a domain name
    # for sender authentication.
    SOA = "SOA"  # Start of [a zone of] authority record : Specifies authoritative information about a DNS zone,
    # including the primary name server, the email of the domain administrator, the domain serial number,
    # and several timers relating to refreshing the zone.
    SRV = "SRV"  # Service locator : Generalized service location record, used for newer protocols instead of
    # creating protocol-specific records such as MX.
    SSHFP = "SSHFP"  # SSH Public Key Fingerprint : Resource record for publishing SSH public host key fingerprints
    # in the DNS, in order to aid in verifying the authenticity of the host.
    SVCB = "SVCB"  # Service Binding : RR that improves performance for clients that need to resolve many
    # resources to access a domain.
    TA = "TA"  # Trust Authorities : Part of a deployment proposal for DNSSEC without a signed DNS root.
    TKEY = "TKEY"  # Transaction Key record : A method of providing keying material to be used with TSIG
    # that is encrypted under the public key in an accompanying KEY RR.
    TLSA = "TLSA"  # TLSA certificate association : A record for DANE. The TLSA DNS resource record is used to
    # associate a TLS server certificate or public key with the domain name where the record is found.
    TSIG = "TSIG"  # Transaction Signature : Can be used to authenticate dynamic updates as coming from an approved
    # client, or to authenticate responses as coming from an approved recursive name server similar to DNSSEC.
    TXT = "TXT"  # Text record : Originally for arbitrary human-readable text in a DNS record. Often carries
    # machine-readable data, such as opportunistic encryption, Sender Policy Framework, DKIM, DMARC, DNS-SD, etc.
    URI = "URI"  # Uniform Resource Identifier : Can be used for publishing mappings from hostnames to URIs.
    ZONEMD = "ZONEMD"  # Message Digests for DNS Zones : Provides a cryptographic message digest over DNS zone data.


class IPUsage(Enum):
    parking = "parking"
    vpn = "vpn"
    tor = "tor"
