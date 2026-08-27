from dataclasses import dataclass
from enum import Enum


class TransactionType(Enum):
    VERIFICATION = "verification"
    IDENTIFICATION = "identification"
    ENROLLMENT = "enrollment"


class ComputationalRequirement(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class TransactionRequest:
    transactions_per_second: int
    transaction_type: TransactionType
    computational_requirement: ComputationalRequirement


@dataclass
class HardwareRequirements:
    cpu_cores: int
    ram_gb: int
    disk_gb: int