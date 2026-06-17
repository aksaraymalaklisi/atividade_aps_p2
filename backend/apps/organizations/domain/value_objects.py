from enum import Enum


class OrganizationStatus(Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class MembershipRole(Enum):
    OWNER = "OWNER"
    LEADER = "LEADER"
    MEMBER = "MEMBER"
