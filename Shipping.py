import json
from enum import Enum

# Definir los Enums
class Shipping_Service(Enum):
    MRW = "MRW"
    Tealca = "Tealca"
    Ipostel = "Ipostel"

class Shipping_Method(Enum):
    Oficina_de_retiro = "Oficina de retiro"
    Puerta_a_Puerta = "Puerta a Puerta"
    Apartado_postal = "Apartado postal"

class Shipping_Status(Enum):
    Procesado = "Procesado"
    En_transito = "En tránsito"
    Entregado = "Entregado"
    Cancelado = "Cancelado"
    Devuelto = "Devuelto"

# Clase Shipping
class Shipping:
    def __init__(self, shipping_service, shipping_method, shipping_status, service_price):
        self.shippingId = self.get_next_shipping_id()
        self.shipping_service = shipping_service
        self.shipping_method = shipping_method
        self.shipping_status = shipping_status
        self.service_price = service_price

    # Método para obtener el próximo shippingId
    @staticmethod
    def get_next_shipping_id(file_name="Shipping.json"):
        try:
            with open(file_name, "r") as file:
                shipments = json.load(file)
                if shipments:
                    return max(shipment["shippingId"] for shipment in shipments) + 1
                else:
                    return 1
        except (FileNotFoundError, json.JSONDecodeError):
            return 1

    # Método para guardar el envío en el archivo JSON
    def create_shipping(self, file_name="Shipping.json"):
        new_shipping = {
            "shippingId": self.shippingId,
            "shipping_service": self.shipping_service.name,
            "shipping_method": self.shipping_method.name,
            "shipping_status": self.shipping_status.name,
            "service_price": self.service_price
        }

        try:
            with open(file_name, "r+") as file:
                shipments = json.load(file)
                shipments.append(new_shipping)
                file.seek(0)
                json.dump(shipments, file, indent=4)
        except (FileNotFoundError, json.JSONDecodeError):
            with open(file_name, "w") as file:
                json.dump([new_shipping], file, indent=4)

    def get_shipping(shipping_id):
        # Leer el archivo JSON y buscar un envío por shippingId
        try:
            with open("Shipping.json", "r") as file:
                data = json.load(file)
                for shipment in data:
                    if shipment['shippingId'] == shipping_id:
                        return shipment
        except FileNotFoundError:
            print("El archivo Shipping.json no existe.")
        return None

