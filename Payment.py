import json
from enum import Enum
from datetime import datetime

# Enums para Currency, Payment_Method, Payment_Status y Payment_Condition
class Currency(Enum):
    USD = "Dolar estadounidense"
    EUR = "Euro"
    CNY = "Yuan Chino"
    GBP = "Libra esterlina"
    CHF = "Franco suizo"
    VEF = "Bolivar"

class Payment_Method(Enum):
    POS = "Punto Venta"
    MOBILE = "Pago Movil"
    TRANSFER = "Transfer"
    ZELLE = "Zelle"
    PAYPAL = "PayPal"
    CASH = "Cash"

class Payment_Status(Enum):
    PROCESSING = "Procesando"
    COMPLETED = "Completado"
    FAILED = "Fallido"
    CANCELED = "Cancelado"
    REFUNDED = "Reembolsado"
    RETURNED = "Devuelto"
    OVERDRAWN = "Sobregirado"
    PENDING = "En espera"
    REJECTED = "Rechazado"

class Payment_Condition(Enum):
    CONTADO = "Contado"
    CREDITO = "Credito"

class Payment:
    FILE_NAME = "Payment.json"

    def __init__(self, paymentId, amount, currency, method, status, date, condition):
        self.paymentId = paymentId
        self.amount = amount
        self.currency = currency
        self.method = method
        self.status = status
        self.date = date
        self.condition = condition

    @classmethod
    def get_next_payment_id(cls):
        try:
            with open(cls.FILE_NAME, 'r') as file:
                payments = json.load(file)
                if payments:
                    last_id = max(payment['paymentId'] for payment in payments)
                    return last_id + 1
        except FileNotFoundError:
            return 1
        return 1

    @classmethod
    def create_payment(cls, amount, currency, method, status, client_type, condition=None):
        paymentId = cls.get_next_payment_id()
        date = datetime.now().isoformat()
        # Determinar Payment_Condition por defecto si no se proporciona
        if not condition:
            if client_type == "Natural_Person":
                condition = Payment_Condition.CONTADO
            elif client_type == "Legal_Entity":
                condition = Payment_Condition.CREDITO if condition == Payment_Condition.CREDITO else Payment_Condition.CONTADO

        payment = {
            "paymentId": paymentId,
            "amount": amount,
            "currency": currency.value,
            "method": method.value,
            "status": status.value,
            "date": date,
            "condition": condition.value
        }
        try:
            with open(cls.FILE_NAME, 'r') as file:
                payments = json.load(file)
        except FileNotFoundError:
            payments = []
        payments.append(payment)
        with open(cls.FILE_NAME, 'w') as file:
            json.dump(payments, file, indent=4)
        return payment

    @classmethod
    def get_payment(cls, paymentId):
        try:
            with open(cls.FILE_NAME, 'r') as file:
                payments = json.load(file)
                for payment in payments:
                    if payment["paymentId"] == paymentId:
                        return payment
        except FileNotFoundError:
            pass
        return None

    @classmethod
    def update_payment(cls, paymentId, **kwargs):
        try:
            with open(cls.FILE_NAME, 'r') as file:
                payments = json.load(file)
            for payment in payments:
                if payment["paymentId"] == paymentId:
                    for key, value in kwargs.items():
                        if key in payment:
                            payment[key] = value
                    break
            with open(cls.FILE_NAME, 'w') as file:
                json.dump(payments, file, indent=4)
            return True
        except FileNotFoundError:
            return False

    @classmethod
    def delete_payment(cls, paymentId):
        try:
            with open(cls.FILE_NAME, 'r') as file:
                payments = json.load(file)
            payments = [payment for payment in payments if payment["paymentId"] != paymentId]
            with open(cls.FILE_NAME, 'w') as file:
                json.dump(payments, file, indent=4)
            return True
        except FileNotFoundError:
            return False



Payment.create_payment(
    amount=500.0,
    currency=Currency.EUR,
    method=Payment_Method.TRANSFER,
    status=Payment_Status.COMPLETED,
    client_type="Legal_Entity",
    condition=Payment_Condition.CREDITO
)
