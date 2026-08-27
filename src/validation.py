from src.models import TransactionRequest


def validate_request(request: TransactionRequest) -> None:
    if request.transactions_per_second <= 0:
        raise ValueError(
            "Transactions per second must be greater than zero."
        )