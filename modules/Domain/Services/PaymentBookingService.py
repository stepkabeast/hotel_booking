from abc import ABC, abstractmethod
from datetime import datetime

class PaymentService(ABC):
    __response: dict

    @abstractmethod
    def create_pay(self) -> dict:
        raise NotImplementedError

class PaymentBookingService(PaymentService):

    def __init__(self, transaction_id: str, status: str, amount: float, currency: str, payment_method: str, authorization_code: str = None, error_code: str = None, error_message: str = None, card: dict = None):
        self._transaction_id = transaction_id
        self._status = status
        self._amount = amount

    def create_pay(self) -> dict:
        return {
            'transaction_id': self._transaction_id,
            'status': self._status,
            'amount': self._amount,
        }