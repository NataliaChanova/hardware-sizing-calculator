from src.models import TransactionType, ComputationalRequirement


TRANSACTION_PROFILES = {
    TransactionType.VERIFICATION: {
        "cpu_per_tps": 0.01,
        "ram_per_tps": 0.02,
        "disk_per_transaction_mb": 0.001,
    },
    TransactionType.IDENTIFICATION: {
        "cpu_per_tps": 0.03,
        "ram_per_tps": 0.05,
        "disk_per_transaction_mb": 0.001,
    },
    TransactionType.ENROLLMENT: {
        "cpu_per_tps": 0.02,
        "ram_per_tps": 0.03,
        "disk_per_transaction_mb": 0.01,
    },
}


COMPUTATIONAL_MULTIPLIERS = {
    ComputationalRequirement.LOW: 0.7,
    ComputationalRequirement.MEDIUM: 1.0,
    ComputationalRequirement.HIGH: 1.5,
}


CPU_SAFETY_MARGIN = 1.2
RAM_SAFETY_MARGIN = 1.2
DISK_SAFETY_MARGIN = 1.3


MIN_CPU_CORES = 1
MIN_RAM_GB = 1
MIN_DISK_GB = 10


RETENTION_DAYS = 30