import json
from enum import Enum
from datetime import datetime

class StatusOrder(Enum):
    PENDIENTE = "Pendiente"
    PAGO_CONFIRMADO = "Pago Confirmado"
    EN_PREPARACION = "En Preparación"
    ENVIADO = "Enviado"
    ENTREGADO = "Entregado"
    CANCELADO = "Cancelado"
    REEMBOLSO_EN_PROCESO = "Reembolso en Proceso"
    DEVUELTO = "Devuelto"

class Order:
    JSON_FILE = "Order.json"

    def __init__(self, purchased_quantity, status, productId, paymentId, shippingId):
        self.orderId = self.get_next_order_id()
        self.purchased_quantity = purchased_quantity
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status = status
        self.productId = productId
        self.paymentId = paymentId
        self.shippingId = shippingId

    @staticmethod
    def get_next_order_id():
        try:
            with open(Order.JSON_FILE, "r") as file:
                orders = json.load(file)
            if orders:
                return max(order["orderId"] for order in orders) + 1
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return 1

    def save(self):
        try:
            with open(Order.JSON_FILE, "r") as file:
                orders = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            orders = []

        orders.append(self.to_dict())

        with open(Order.JSON_FILE, "w") as file:
            json.dump(orders, file, indent=4)

    @staticmethod
    def read_all():
        try:
            with open(Order.JSON_FILE, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def get_order(orderId):
        orders = Order.read_all()
        for order in orders:
            if order["orderId"] == orderId:
                return order
        return None

    @staticmethod
    def update(orderId, **kwargs):
        orders = Order.read_all()
        updated = False
        for order in orders:
            if order["orderId"] == orderId:
                for key, value in kwargs.items():
                    if key in order:
                        order[key] = value
                updated = True
                break
        if updated:
            with open(Order.JSON_FILE, "w") as file:
                json.dump(orders, file, indent=4)
        return updated

    @staticmethod
    def delete(orderId):
        orders = Order.read_all()
        orders = [order for order in orders if order["orderId"] != orderId]
        with open(Order.JSON_FILE, "w") as file:
            json.dump(orders, file, indent=4)

    def to_dict(self):
        return {
            "orderId": self.orderId,
            "purchased_quantity": self.purchased_quantity,
            "date": self.date,
            "status": self.status.value,
            "productId": self.productId,
            "paymentId": self.paymentId,
            "shippingId": self.shippingId,
        }

# Crear órdenes
# order1 = Order(2, StatusOrder.PENDIENTE, 101, 201, 301)
#order1.save()

# order2 = Order(1, StatusOrder.PAGO_CONFIRMADO, 102, 202, 302)
# order2.save()


# Leer una orden específica
# print("\nOrden con ID 1:")
# print(Order.get_order(1))

# Leer todas las órdenes
# print("Todas las órdenes:")
# print(Order.read_all())

# Actualizar una Order
# print("\nActualizando la orden con ID 1...")
# Order.update(1, status=StatusOrder.EN_PREPARACION.value)
# print(Order.get_order(1))

# Eliminar una Orden
# print("\nEliminando la orden con ID 2...")
# Order.delete(2)
#print(Order.read_all())
