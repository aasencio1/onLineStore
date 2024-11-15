import requests
import os
import json
from Product import Product  # Asegúrate de que Product.py esté en el mismo directorio o en el path

class Main:
    def __init__(self, url):
        self.url = url
        self.data = None
        self.running = True
       # self.product_instance = Product() 

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def LoadData(self):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                self.data = response.json()  # Asumiendo que el contenido de la URL es JSON
                print("Data loaded successfully.")
                
                # Crear instancia de Product pasando self.data
                product = Product(self.data)

                # Guardar datos en archivo JSON
                product.DataStorage()
             
            else:
                print(f"Error: Unable to load data. Status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
        except json.JSONDecodeError:
            print("Error: Data is not in JSON format.")

    def main_menu(self):
        while self.running:
            self.clear_terminal()
            print("\n--- Menú Principal ---")
            print("1. Producto")
            print("2. Cliente")
            print("3. Salir")
            choice = input("Seleccione una opción: ")

            if choice == "1":
                self.product_menu()
            elif choice == "2":
                self.client_menu()
            elif choice == "3":
                print("Saliendo del sistema...")
                self.running = False
            else:
                print("Opción no válida. Intente de nuevo.")

    def product_menu(self):
        while True:
            self.clear_terminal()
            print("\n--- Menú de Producto ---")
            print("1. Agregar Producto")
            print("2. Buscar Producto")
            print("3. Actualizar Producto")
            print("4. Eliminar Producto")
            print("5. Retornar al Menú Principal")
            choice = input("Seleccione una opción: ")

            if choice == "1":
                self.add_product()
            elif choice == "2":
                #self.read_product()
                Product.list_all_products()
            elif choice == "3":
                self.update_product()
            elif choice == "4":
                self.delete_product()
            elif choice == "5":
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    def add_product(self):
        try:
            nuevo_producto = {
                'product_id': int(input("Ingrese el ID del producto: ")),
                'name': input("Ingrese el nombre del producto: "),
                'description': input("Ingrese la descripción del producto: "),
                'price': float(input("Ingrese el precio del producto: ")),
                'category': input("Ingrese la categoría del producto: "),
                'inventory': int(input("Ingrese el inventario del producto: ")),
                'compatible_vehicles': input("Ingrese los vehículos compatibles (separados por comas): ").split(",")
            }
            Product.create_product(nuevo_producto)
        except ValueError:
            print("Error: Asegúrese de ingresar valores válidos para el ID, precio e inventario.")

    def read_product(self):
        try:
           
            product_id = int(input("Ingrese el ID del producto a buscar: "))
            producto_leido = Product.get_product(product_id)
            if producto_leido:
                print("Producto encontrado:")
                print(f"ID: {producto_leido['product_id']}")
                print(f"Nombre: {producto_leido['name']}")
                print(f"Descripción: {producto_leido['description']}")
                print(f"Precio: {producto_leido['price']}")
                print(f"Categoría: {producto_leido['category']}")
                print(f"Inventario: {producto_leido['inventory']}")
                print(f"Vehículos compatibles: {', '.join(producto_leido['compatible_vehicles'])}")
            else:
                    print("Producto no encontrado.")
            #if producto_leido:
            #    print("\nDetalles del Producto:")
            #    for key, value in producto_leido.items():
            #        print(f"{key}: {value}")
        except ValueError:
            print("Error: Asegúrese de ingresar un ID válido.")

    def update_product(self):
        try:
            product_id = int(input("Ingrese el ID del producto a actualizar: "))
            updated_data = {
                'name': input("Ingrese el nuevo nombre (deje en blanco para no cambiar): "),
                'description': input("Ingrese la nueva descripción (deje en blanco para no cambiar): "),
                'price': float(input("Ingrese el nuevo precio (deje en blanco para no cambiar): ") or 0),
                'category': input("Ingrese la nueva categoría (deje en blanco para no cambiar): "),
                'inventory': int(input("Ingrese el nuevo inventario (deje en blanco para no cambiar): ") or 0),
                'compatible_vehicles': input("Ingrese los nuevos vehículos compatibles (separados por comas, deje en blanco para no cambiar): ").split(",") if input else None
            }
            Product.update_product(product_id, {k: v for k, v in updated_data.items() if v})
        except ValueError:
            print("Error: Asegúrese de ingresar valores válidos.")

    def delete_product(self):
        try:
            product_id = int(input("Ingrese el ID del producto a eliminar: "))
            Product.delete_product(product_id)
        except ValueError:
            print("Error: Asegúrese de ingresar un ID válido.")

# Ejecución del programa
if __name__ == "__main__":
    url = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/products.json"  # URL de ejemplo
    main_app = Main(url)
    main_app.LoadData()  # Cargar los datos y ejecutar el método DataStorage
    main_app.main_menu()
#Product.list_all_products()

   


