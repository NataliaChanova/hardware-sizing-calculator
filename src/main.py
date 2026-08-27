import argparse

from src.calculator import calculate_requirements
from src.models import (
    TransactionRequest,
    TransactionType,
    ComputationalRequirement,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Estimate hardware requirements for a given transaction load."
    )
    parser.add_argument(
        "--tps",
        type=int,
        help="Transactions per second (whole number > 0).",
    )
    parser.add_argument(
        "--type",
        dest="transaction_type",
        choices=[item.value for item in TransactionType],
        help="Transaction type.",
    )
    parser.add_argument(
        "--requirement",
        dest="computational_requirement",
        choices=[item.value for item in ComputationalRequirement],
        help="Computational requirement of a transaction.",
    )
    return parser.parse_args()


def get_transactions_per_second() -> int:
    while True:
        try:
            value = int(input("Transactions per second: "))

            if value <= 0:
                print("Error: Transactions per second must be greater than zero.")
                continue

            return value

        except ValueError:
            print("Error: Transactions per second must be a whole number.")


def get_transaction_type() -> TransactionType:
    while True:
        value = input(
            "Transaction type "
            "[verification/identification/enrollment]: "
        ).strip().lower()

        try:
            return TransactionType(value)
        except ValueError:
            print(
                "Error: Invalid transaction type. "
                "Choose verification, identification, or enrollment."
            )


def get_computational_requirement() -> ComputationalRequirement:
    while True:
        value = input(
            "Computational requirement "
            "[low/medium/high]: "
        ).strip().lower()

        try:
            return ComputationalRequirement(value)
        except ValueError:
            print(
                "Error: Invalid computational requirement. "
                "Choose low, medium, or high."
            )


def main():
    args = parse_args()

    if args.tps is not None:
        if args.tps <= 0:
            print("Error: Transactions per second must be greater than zero.")
            return
        transactions_per_second = args.tps
    else:
        transactions_per_second = get_transactions_per_second()

    if args.transaction_type is not None:
        transaction_type = TransactionType(args.transaction_type)
    else:
        transaction_type = get_transaction_type()

    if args.computational_requirement is not None:
        computational_requirement = ComputationalRequirement(
            args.computational_requirement
        )
    else:
        computational_requirement = get_computational_requirement()

    request = TransactionRequest(
        transactions_per_second=transactions_per_second,
        transaction_type=transaction_type,
        computational_requirement=computational_requirement,
    )

    try:
        result = calculate_requirements(request)
    except ValueError as error:
        print(f"Error: {error}")
        return

    print("\nHardware requirements:")
    print(f"CPU cores: {result.cpu_cores}")
    print(f"RAM: {result.ram_gb} GB")
    print(f"Disk: {result.disk_gb} GB")


if __name__ == "__main__":
    main()