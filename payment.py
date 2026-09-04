import functools
import uuid
from abc import ABC, abstractmethod
from datetime import datetime


# =====================================================================
# 1. STRATEGY INTERFACE
# =====================================================================

class PaymentStrategy(ABC):
    """
    Common interface for all payment methods.
    Every payment method must implement validate() and pay().
    """

    name = "Generic Payment"

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def pay(self, amount):
        pass

    def _make_receipt(self, amount, status="SUCCESS"):
        """Create a simple payment receipt."""
        return {
            "transaction_id": str(uuid.uuid4())[:8],
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "payment_method": self.name,
            "amount": amount,
            "status": status
        }


# =====================================================================
# 2. CREDIT CARD PAYMENT
# =====================================================================

class CreditCardPayment(PaymentStrategy):

    name = "Credit Card"

    def __init__(self, card_number, cvv, expiry):
        self.card_number = card_number
        self.cvv = cvv
        self.expiry = expiry

    def validate(self):
        return (
            self.card_number.isdigit()
            and len(self.card_number) == 16
            and self.cvv.isdigit()
            and len(self.cvv) == 3
            and len(self.expiry) == 5
        )

    def pay(self, amount):
        if not self.validate():
            return self._make_receipt(
                amount,
                status="FAILED - Invalid Card Details"
            )

        print(
            f" -> Charging Rs.{amount:.2f} "
            f"to Credit Card ending {self.card_number[-4:]}"
        )

        return self._make_receipt(amount)


# =====================================================================
# 3. PAYPAL PAYMENT
# =====================================================================

class PayPalPayment(PaymentStrategy):

    name = "PayPal"

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def validate(self):
        return (
            "@" in self.email
            and "." in self.email
            and len(self.password) >= 4
        )

    def pay(self, amount):
        if not self.validate():
            return self._make_receipt(
                amount,
                status="FAILED - Invalid PayPal Details"
            )

        print(
            f" -> Paying Rs.{amount:.2f} "
            f"using PayPal account {self.email}"
        )

        return self._make_receipt(amount)


# =====================================================================
# 4. UPI PAYMENT
# =====================================================================

class UPIPayment(PaymentStrategy):

    name = "UPI"

    def __init__(self, upi_id):
        self.upi_id = upi_id

    def validate(self):
        return (
            "@" in self.upi_id
            and len(self.upi_id.split("@")[0]) > 0
            and len(self.upi_id.split("@")[1]) > 0
        )

    def pay(self, amount):
        if not self.validate():
            return self._make_receipt(
                amount,
                status="FAILED - Invalid UPI ID"
            )

        print(
            f" -> Paying Rs.{amount:.2f} "
            f"using UPI ID {self.upi_id}"
        )

        return self._make_receipt(amount)


# =====================================================================
# 5. NET BANKING PAYMENT
# =====================================================================

class NetBankingPayment(PaymentStrategy):

    name = "Net Banking"

    def __init__(self, bank_name, account_number):
        self.bank_name = bank_name
        self.account_number = account_number

    def validate(self):
        return (
            self.account_number.isdigit()
            and len(self.account_number) >= 9
        )

    def pay(self, amount):
        if not self.validate():
            return self._make_receipt(
                amount,
                status="FAILED - Invalid Account Number"
            )

        print(
            f" -> Debiting Rs.{amount:.2f} "
            f"from {self.bank_name} A/C {self.account_number}"
        )

        return self._make_receipt(amount)


# =====================================================================
# 6. DECORATOR - TRANSACTION LOGGING
# =====================================================================

def log_transaction(func):
    """
    Decorator that logs the start and result of every payment.
    """

    @functools.wraps(func)
    def wrapper(self, amount, *args, **kwargs):

        method = self.strategy.name if self.strategy else "NONE"

        print(
            f"\n[LOG] Initiating payment of "
            f"Rs.{amount:.2f} via {method}"
        )

        try:
            result = func(self, amount, *args, **kwargs)

            print(
                f"[LOG] Payment completed with status: "
                f"{result['status']}"
            )

            return result

        except Exception as e:
            print(f"[LOG] Payment failed: {e}")
            raise

    return wrapper


# =====================================================================
# 7. CONTEXT CLASS
# =====================================================================

class PaymentProcessor:
    """
    Context of the Strategy Pattern.

    It stores the currently selected payment strategy
    and delegates payment processing to that strategy.
    """

    _registry = {}

    def __init__(self, strategy=None):
        self.strategy = strategy

    def set_strategy(self, strategy):
        """Change payment method at runtime."""

        self.strategy = strategy

        print(
            f"[CONFIG] Payment method switched to: "
            f"{strategy.name}"
        )

    @log_transaction
    def process_payment(self, amount):

        if self.strategy is None:
            raise ValueError(
                "No payment strategy configured "
                "on this processor"
            )

        if amount <= 0:
            raise ValueError(
                "Payment amount must be greater than zero"
            )

        return self.strategy.pay(amount)

    # -----------------------------------------------------------------
    # Registry methods
    # -----------------------------------------------------------------

    @classmethod
    def register_strategy(cls, key, strategy_cls):
        """Register a payment strategy."""

        cls._registry[key] = strategy_cls

        print(
            f"[REGISTRY] '{key}' -> "
            f"{strategy_cls.__name__} registered"
        )

    @classmethod
    def available_methods(cls):
        """Return all registered payment methods."""

        return list(cls._registry.keys())

    @classmethod
    def create(cls, key, **kwargs):
        """
        Create a PaymentProcessor using a registered strategy.
        """

        if key not in cls._registry:
            raise ValueError(
                f"No payment strategy registered under '{key}'"
            )

        strategy_class = cls._registry[key]

        strategy = strategy_class(**kwargs)

        return cls(strategy)


# =====================================================================
# 8. DEMO / DRIVER CODE
# =====================================================================

if __name__ == "__main__":

    # ---------------------------------------------------------------
    # Step A: Register payment strategies
    # ---------------------------------------------------------------

    PaymentProcessor.register_strategy(
        "credit_card",
        CreditCardPayment
    )

    PaymentProcessor.register_strategy(
        "paypal",
        PayPalPayment
    )

    PaymentProcessor.register_strategy(
        "upi",
        UPIPayment
    )

    PaymentProcessor.register_strategy(
        "netbanking",
        NetBankingPayment
    )

    print(
        "\nAvailable payment methods:",
        PaymentProcessor.available_methods()
    )


    # ---------------------------------------------------------------
    # Step B: Create processor using UPI
    # ---------------------------------------------------------------

    processor = PaymentProcessor.create(
        "upi",
        upi_id="rahul@okhdfcbank"
    )

    receipt1 = processor.process_payment(1500)

    print("Receipt:", receipt1)


    # ---------------------------------------------------------------
    # Step C: Switch to Credit Card
    # ---------------------------------------------------------------

    print("\n--- Switching to Credit Card ---")

    processor.set_strategy(
        CreditCardPayment(
            "1234567812345678",
            "123",
            "12/27"
        )
    )

    receipt2 = processor.process_payment(2500)

    print("Receipt:", receipt2)


    # ---------------------------------------------------------------
    # Step D: Try invalid PayPal
    # ---------------------------------------------------------------

    print("\n--- Switching to Invalid PayPal ---")

    processor.set_strategy(
        PayPalPayment(
            "bad-email",
            "123"
        )
    )

    receipt3 = processor.process_payment(500)

    print("Receipt:", receipt3)


    # ---------------------------------------------------------------
    # Step E: Switch to Net Banking
    # ---------------------------------------------------------------

    print("\n--- Switching to Net Banking ---")

    processor.set_strategy(
        NetBankingPayment(
            "State Bank",
            "987654321"
        )
    )

    receipt4 = processor.process_payment(999.50)

    print("Receipt:", receipt4)