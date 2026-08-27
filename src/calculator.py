
import math

from src.validation import validate_request
from src.constants import (
    TRANSACTION_PROFILES,
    COMPUTATIONAL_MULTIPLIERS,
    CPU_SAFETY_MARGIN,
    RAM_SAFETY_MARGIN,
    DISK_SAFETY_MARGIN,
    MIN_CPU_CORES,
    MIN_RAM_GB,
    MIN_DISK_GB,
    RETENTION_DAYS,
)
from src.models import TransactionRequest, HardwareRequirements

def calculate_requirements(
    request: TransactionRequest,
) -> HardwareRequirements:
    validate_request(request)

    profile = TRANSACTION_PROFILES[request.transaction_type]

    computational_multiplier = COMPUTATIONAL_MULTIPLIERS[
        request.computational_requirement
    ]

    cpu = (
        request.transactions_per_second
        * profile["cpu_per_tps"]
        * computational_multiplier
        * CPU_SAFETY_MARGIN
    )

    ram = (
        request.transactions_per_second
        * profile["ram_per_tps"]
        * computational_multiplier
        * RAM_SAFETY_MARGIN
    )

    seconds_per_day = 24 * 60 * 60

    total_transactions = (
        request.transactions_per_second
        * seconds_per_day
        * RETENTION_DAYS
    )

    disk_mb = (
        total_transactions
        * profile["disk_per_transaction_mb"]
        * DISK_SAFETY_MARGIN
    )

    disk_gb = disk_mb / 1024

    return HardwareRequirements(
        cpu_cores=max(math.ceil(cpu), MIN_CPU_CORES),
        ram_gb=max(math.ceil(ram), MIN_RAM_GB),
        disk_gb=max(math.ceil(disk_gb), MIN_DISK_GB),
    )
