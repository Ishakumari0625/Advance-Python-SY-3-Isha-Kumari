class CreditCard:
    def pay(self, amount):
        print("Paid", amount, "using Credit Card")

class UPI:
    def pay(self, amount):
        print("Paid", amount, "using UPI")

class NetBanking:
    def pay(self, amount):
        print("Paid", amount, "using Net Banking")

class Payment:
    def __init__(self, strategy):
        self.strategy = strategy

    def process(self, amount):
        self.strategy.pay(amount)

amount = float(input("Enter amount: "))
choice = input("Enter payment method (card/upi/bank): ").lower()

if choice == "card":
    p = Payment(CreditCard())
elif choice == "upi":
    p = Payment(UPI())
elif choice == "bank":
    p = Payment(NetBanking())
else:
    print("Invalid payment method")
    exit()

p.process(amount)