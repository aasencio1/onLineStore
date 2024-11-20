import json
from enum import Enum
from datetime import datetime
from bokeh.plotting import figure, show
from bokeh.io import output_notebook
from bokeh.models import ColumnDataSource
from datetime import datetime, timedelta

class StatusOrder(Enum):
    PENDIENTE = "Pendiente"
    PAGO_CONFIRMADO = "Pago Confirmado"
    EN_PREPARACION = "En Preparacion"
    ENVIADO = "Enviado"
    ENTREGADO = "Entregado"
    CANCELADO = "Cancelado"
    REEMBOLSO_EN_PROCESO = "Reembolso en Proceso"
    DEVUELTO = "Devuelto"

class ClientType(Enum):
    NATURAL_PERSON = "Natural_Person"
    LEGAL_ENTITY = "Legal_Entity"

class Order:
    JSON_FILE = "Order.json"

    def __init__(self, purchased_quantity, status, productId, paymentId, shippingId, identification, client_type):
        self.orderId = self.get_next_order_id()
        self.purchased_quantity = purchased_quantity
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status = status
        self.productId = productId
        self.paymentId = paymentId
        self.shippingId = shippingId
        self.identification = identification
        self.client_type = client_type

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

    def create_order(self):
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
    def get_order_by_identification(identification):
        """
        Obtiene una lista de órdenes asociadas a una identificación específica.
        
        :param identification: Identificación del cliente (Natural o Jurídico).
        :return: Lista de órdenes que coinciden con la identificación.
        """
        orders = Order.read_all()
        matched_orders = [order for order in orders if order["identification"] == identification]
        return matched_orders if matched_orders else None
    
    @staticmethod
    def get_orders_by_date(input_date):
        """
        Busca órdenes por fecha, ignorando la hora.
        
        :param input_date: Fecha en formato 'dd/mm/aaaa'.
        :return: Lista de órdenes que coinciden con la fecha o None si no hay coincidencias.
        """
        try:
            # Convertir la fecha de entrada al formato almacenado en JSON
            formatted_date = datetime.strptime(input_date, "%d/%m/%Y").strftime("%Y-%m-%d")
            orders = Order.read_all()
            matched_orders = [order for order in orders if order["date"].startswith(formatted_date)]
            return matched_orders if matched_orders else None
        except ValueError:
            print("Formato de fecha inválido. Use dd/mm/aaaa.")
            return None
        
    @staticmethod
    def get_total_sales(group_by="day"):
        """
        Calcula las ventas totales agrupadas por día, mes o año.

        :param group_by: Define la agrupación ('day', 'month', 'year').
        :return: Diccionario con las ventas totales agrupadas.
        """
        try:
            # Leer todas las órdenes
            orders = Order.read_all()
            with open("data.json", "r") as product_file:
                products = {product["id"]: product for product in json.load(product_file)}

            sales_summary = {}

            for order in orders:
                date_key = None
                order_date = datetime.strptime(order["date"], "%Y-%m-%d %H:%M:%S")

                if group_by == "day":
                    date_key = order_date.strftime("%Y-%m-%d")
                elif group_by == "month":
                    date_key = order_date.strftime("%Y-%m")
                elif group_by == "year":
                    date_key = order_date.strftime("%Y")
                else:
                    raise ValueError("El parámetro 'group_by' debe ser 'day', 'month' o 'year'.")

                product = products.get(order["productId"])
                if product:
                    total_order_value = product["price"] * order["purchased_quantity"]
                    sales_summary[date_key] = sales_summary.get(date_key, 0) + total_order_value

            return sales_summary
        except FileNotFoundError:
            print("Archivo no encontrado. Asegúrate de que los datos están disponibles.")
            return {}


 @staticmethod
    def visualize_sales_by_period(json_file, group_by="day"):
        """
        Visualiza las ventas totales agrupadas por día, semana o año usando Bokeh.

        :param json_file: Ruta del archivo JSON con los datos de ventas.
        :param group_by: Período de agrupación ('day', 'week', 'year').
        """
        try:
            with open(json_file, "r") as file:
                sales_data = json.load(file)

            # Preparar los datos para Bokeh
            periods = sorted(sales_data.keys())
            totals = [sales_data[period] for period in periods]

            source = ColumnDataSource(data=dict(periods=periods, totals=totals))

            # Configurar el gráfico
            title = f"Ventas Totales por {group_by.capitalize()}"
            p = figure(
                x_range=periods,
                height=400,
                width=800,
                title=title,
                toolbar_location=None,
                tools=""
            )
            p.vbar(x="periods", top="totals", width=0.8, source=source)
            p.xgrid.grid_line_color = None
            p.y_range.start = 0
            p.xaxis.major_label_orientation = 0.5
            p.yaxis.axis_label = "Total Ventas ($)"
            p.xaxis.axis_label = f"Período ({group_by.capitalize()})"

            # Mostrar el gráfico
            show(p)

        except FileNotFoundError:
            print(f"El archivo {json_file} no existe. Asegúrate de generarlo previamente.")
        except Exception as e:
            print(f"Error al generar la visualización: {e}")

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
            "identification": self.identification,
            "client_type": self.client_type.value,
        }

# Ejemplos CRUD

# Crear órdenes
#order1 = Order(2, StatusOrder.PENDIENTE, 101, 201, 301, "123456789", ClientType.NATURAL_PERSON)
#order1.create_order()

#order2 = Order(1, StatusOrder.PAGO_CONFIRMADO, 102, 202, 302, "J-987654321", ClientType.LEGAL_ENTITY)
#order2.create_order()

# Leer todas las órdenes
#print("Todas las órdenes:")
#print(Order.read_all())


# Leer una orden específica
#print("\nOrden con ID 1:")
#print(Order.get_order(1))

# Actualizar una orden
#print("\nActualizando la orden con ID 1...")
#Order.update(1, status=StatusOrder.EN_PREPARACION.value, client_type=ClientType.LEGAL_ENTITY.value)
#print(Order.get_order(1))

# Eliminar una orden
#print("\nEliminando la orden con ID 2...")
#Order.delete(2)
#print(Order.read_all())

#order1 = Order(2, StatusOrder.PENDIENTE, 101, 201, 301, "123456789", ClientType.NATURAL_PERSON)
#order1.create_order()

#order2 = Order(1, StatusOrder.PAGO_CONFIRMADO, 102, 202, 302, "123456789", ClientType.NATURAL_PERSON)
#order2.create_order()

#order3 = Order(1, StatusOrder.ENVIADO, 103, 203, 303, "J-987654321", ClientType.LEGAL_ENTITY)
#order3.create_order()

#print("\nÓrdenes con identificación '123456789':")
#print(Order.get_order_by_identification("123456789"))

#print("\nÓrdenes con identificación 'J-987654321':")
#print(Order.get_order_by_identification("J-987654321"))

#print("\nÓrdenes con identificación inexistente '000000000':")
#print(Order.get_order_by_identification("000000000"))

#fecha_busqueda = "17/11/2024"  # Ingresar la fecha en formato dd/mm/aaaa
#resultados = Order.get_orders_by_date(fecha_busqueda)

#if resultados:
 #   print(f"Órdenes encontradas para la fecha {fecha_busqueda}:")
 #   for order in resultados:
  #      print(order)
#else:
#    print(f"No se encontraron órdenes para la fecha {fecha_busqueda}.")

#sales_by_day = Order.get_total_sales(group_by="day")
#print("Ventas totales por día:")
#for day, total in sales_by_day.items():
 #   print(f"{day}: ${total:.2f}")


#sales_by_month = Order.get_total_sales(group_by="month")
#print("\nVentas totales por mes:")
#for month, total in sales_by_month.items():
#    print(f"{month}: ${total:.2f}")

#sales_by_year = Order.get_total_sales(group_by="year")
#print("\nVentas totales por año:")
#for year, total in sales_by_year.items():
#    print(f"{year}: ${total:.2f}")

Order.visualize_sales_by_period("sales_by_day.json", group_by="day")