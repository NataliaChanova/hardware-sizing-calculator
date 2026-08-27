import sys
from pathlib import Path
import pytest

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.calculator import calculate_requirements
from src.models import (
    TransactionRequest,
    TransactionType,
    ComputationalRequirement,
)


def test_identification_high_requirements():
    request = TransactionRequest(
        transactions_per_second=100,
        transaction_type=TransactionType.IDENTIFICATION,
        computational_requirement=ComputationalRequirement.HIGH,
    )

    result = calculate_requirements(request)

    assert result.cpu_cores == 6
    assert result.ram_gb == 9
    assert result.disk_gb == 330


def test_verification_low_requirements():
    request = TransactionRequest(
        transactions_per_second=10,
        transaction_type=TransactionType.VERIFICATION,
        computational_requirement=ComputationalRequirement.LOW,
    )

    result = calculate_requirements(request)

    assert result.cpu_cores == 1
    assert result.ram_gb == 1
    assert result.disk_gb == 33


def test_enrollment_high_requirements():
    request = TransactionRequest(
        transactions_per_second=10,
        transaction_type=TransactionType.ENROLLMENT,
        computational_requirement=ComputationalRequirement.HIGH,
    )

    result = calculate_requirements(request)

    assert result.cpu_cores == 1
    assert result.ram_gb == 1
    assert result.disk_gb == 330


def test_zero_tps_is_invalid():
    request = TransactionRequest(
        transactions_per_second=0,
        transaction_type=TransactionType.IDENTIFICATION,
        computational_requirement=ComputationalRequirement.HIGH,
    )

    with pytest.raises(ValueError, match="Transactions per second must be greater than zero."):
        calculate_requirements(request)


def test_negative_tps_is_invalid():
    request = TransactionRequest(
        transactions_per_second=-10,
        transaction_type=TransactionType.IDENTIFICATION,
        computational_requirement=ComputationalRequirement.HIGH,
    )

    with pytest.raises(ValueError, match="Transactions per second must be greater than zero."):
        calculate_requirements(request)