import pytest

from src.main import (
    get_transactions_per_second,
    get_transaction_type,
    get_computational_requirement,
    main,
)
from src.models import TransactionType, ComputationalRequirement


def test_get_transactions_per_second(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "100")

    result = get_transactions_per_second()

    assert result == 100


def test_get_transactions_per_second_rejects_invalid_input(monkeypatch):
    inputs = iter(["abc", "0", "-10", "100"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = get_transactions_per_second()

    assert result == 100


def test_get_transaction_type(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "IDENTIFICATION")

    result = get_transaction_type()

    assert result == TransactionType.IDENTIFICATION


def test_get_computational_requirement(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "HIGH")

    result = get_computational_requirement()

    assert result == ComputationalRequirement.HIGH


def test_main_non_interactive_mode_skips_prompts(monkeypatch, capsys):
    monkeypatch.setattr(
        "sys.argv",
        ["main.py", "--tps", "100", "--type", "identification", "--requirement", "high"],
    )

    def fail_if_called(_):
        raise AssertionError("input() should not be called when all args are provided")

    monkeypatch.setattr("builtins.input", fail_if_called)

    main()

    output = capsys.readouterr().out
    assert "CPU cores: 6" in output
    assert "RAM: 9 GB" in output
    assert "Disk: 330 GB" in output


def test_main_non_interactive_rejects_non_positive_tps(monkeypatch, capsys):
    monkeypatch.setattr(
        "sys.argv",
        ["main.py", "--tps", "0", "--type", "identification", "--requirement", "high"],
    )

    main()

    output = capsys.readouterr().out
    assert "Error: Transactions per second must be greater than zero." in output