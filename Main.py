import requests 
import os
import json
from Product import Product  # Asegúrate de que Product.py esté en el mismo directorio o en el path
from Client import Client
from Natural_Person import Natural_Person
from Legal_Entity import Legal_Entity

#, Legal_Entity


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
            print("5. Listar Productos")
            print("6. Retornar al Menú Principal")
            choice = input("Seleccione una opción: ")

            if choice == "1":
                self.add_product()
            elif choice == "2":
                self.read_product()
                
            elif choice == "3":
                self.update_product()
            elif choice == "4":
                self.delete_product()
            elif choice == "5":
                Product.list_all_products()
            elif choice == "6":
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
            #Product.list_all_products()
            self.clear_terminal()
            product_id = int(input("Ingrese el ID del producto a buscar: "))
            producto_leido = Product.get_product(product_id)
           
           #print(f"Este es Producto a Buscar -> { producto_leido['name']}")
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
            input("Presione cualquier tecla para continuar...")
            
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
           # Product.update_product(5, price=1, inventory=2)
           # Product.update_product(product_id, updated_data)

           # Filtrar los datos válidos para evitar cambios no deseados
            filtered_data = {key: value for key, value in updated_data.items() if value}

            # Invocar el método de actualización con los datos capturados
            Product.update_product(product_id, **filtered_data)
            input("Presione cualquier tecla para continuar...")
        except ValueError:
            print("Error: Asegúrese de ingresar valores válidos.")
            input("Presione cualquier tecla para continuar...")

    def delete_product(self):
        try:
            product_id = int(input("Ingrese el ID del producto a eliminar: "))
            Product.delete_product(product_id)
            #input("Presione cualquier tecla para continuar...")
        except ValueError:
            print("Error: Asegúrese de ingresar un ID válido.")
           # input("Presione cualquier tecla para continuar...")
    # Menu Cliente
    def client_menu(self):
        while True:
            self.clear_terminal()
            print("\n--- Menú de Cliente ---")
            print("1. Persona Natural")
            print("2. Persona Jurídica")
            print("3. Retornar al Menú Principal")
            choice = input("Seleccione una opción: ")

            if choice == "1":
                self.natural_person_menu()
            elif choice == "2":
                self.legal_entity_menu()
            elif choice == "3":
                print("Retornando al Menú Principal.")
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    def natural_person_menu(self):
        while True:
            self.clear_terminal()
            print("\n--- Cliente Persona Natural ---")
            print("1. Agregar Cliente")
            print("2. Buscar Cliente")
            print("3. Actualizar Cliente")
            print("4. Eliminar Cliente")
            print("5. Retornar al Menú Anterior")
            choice = input("Seleccione una opción: ")

            if choice == "1":
                print("Agregar Cliente Persona Natural seleccionado.")
                input("Se va ingresar el Cliente ... Conti.......")
                #Nat_person = Natural_Person(
                #        "123 Main St",  # shipping_address
                #        "555-1234",     # phone_number
                #        "email@example.com",  # email
                #        "V-12345678",    # identification
                #        "John",          # name
                #        "Doe"            # last_name
                #    )
                #Natural_Person.create(Nat_person)
                identification = input("Identificación: ")
                name = input("Nombre: ")
                last_name = input("Apellido: ")
                email = input("Correo electrónico: ")
                phone_number = input("Número de teléfono: ")
                shipping_address = input("Dirección de envío: ")
               
                person = Natural_Person(
                        shipping_address,
                        phone_number,
                        email,
                        name,
                        last_name,
                        identification
                    )

                    # Llamar al método create para guardar la instancia
                Natural_Person.create(person)
                print("Cliente Natural agregado exitosamente.")
                input("Presione cualquier tecla para continuar...")
            
            elif choice == "2":
                natural_file = "Natural_Person.json"
                print("Buscar Cliente Persona Natural seleccionado.")
                identification = input("Identificación: ")
                #print(Natural_Person.read(identification , natural_file))
                #input("Presione cualquier tecla para continuar...")

                cliente_Leido= Natural_Person.get_client(identification , natural_file)
                if cliente_Leido:
                    self.clear_terminal()
                    print("Cliente encontrado:")
                    print(f"Identificacion: {cliente_Leido['identification']}")
                    print(f"Nombre: {cliente_Leido['name']}")
                    print(f"Apellido: {cliente_Leido['last_name']}")
                    print(f"Correo-e: {cliente_Leido['email']}")
                    print(f"Número de Teléfono: {cliente_Leido['phone_number']}")
                    print(f"Direccion de envio: {cliente_Leido['shipping_address']}")
                  
                else:
                     print("Cliente no encontrado.")
                input("Presione cualquier tecla para continuar...")



                # Lógica para buscar cliente persona natural
            elif choice == "3":
                natural_file = "Natural_Person.json"
                print("Actualizar Cliente Persona Natural seleccionado.")
                # Lógica para actualizar cliente persona natural
                identifier = input("Ingrese la identificación del cliente a actualizar: ")
                client = Natural_Person.get_client(identifier, natural_file)
                if client:
                    
                        print("Ingrese los nuevos datos (deje en blanco para mantener el actual):")
                        new_name = input(f"Nuevo Nombre ({client.get('name')}): ") or client.get("name")
                        new_last_name = input(f"Nuevo Apellido ({client.get('last_name')}): ") or client.get("last_name")
                        new_email = input(f"Nuevo Email ({client.get('email')}): ") or client.get("email")
                        new_phone = input(f"Nuevo Teléfono ({client.get('phone_number')}): ") or client.get("phone_number")
                        new_address = input(f"Nueva Dirección de Envío ({client.get('shipping_address')}): ") or client.get("shipping_address")
                        
                        updated_data = {
                            "name": new_name,
                            "last_name": new_last_name,
                            "email": new_email,
                            "phone_number": new_phone,
                            "shipping_address": new_address
                        }
                        #Natural_Person.update(identifier, updated_data, natural_file)
                        Client.update(identifier, updated_data, natural_file)
                else:
                        print(f"Cliente con identificación '{identifier}' no encontrado.")
            elif choice == "4":
                natural_file = "Natural_Person.json"
                print("Eliminar Cliente Persona Natural seleccionado.")
                # Lógica para eliminar cliente persona natural
                identifier = input("Ingrese el número de Identificación del Cliente a Eliminar: ")
               
                client= Natural_Person.get_client(identifier , natural_file)
                if client:
                       
                        confirm = input(f"¿Está seguro que desea eliminar al cliente con identificación '{identifier}'? (s/n): ").lower()
                        if confirm == 's':
                            Client.delete_client(identifier, natural_file)
                            print("Cliente Eliminado.")
                            input("Presione cualquier tecla para continuar...")
                        else:
                            print("Operación cancelada.")
                else:
                        print(f"Cliente con identificación '{identifier}' no encontrado.")     
                        input("Presione cualquier tecla para continuar...")
                
            elif choice == "5":
                print("Retornando al Menú de Cliente.")
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    def legal_entity_menu(self):
        while True:
            self.clear_terminal()
            print("\n--- Cliente Persona Jurídica ---")
            print("1. Agregar Cliente")
            print("2. Buscar Cliente")
            print("3. Actualizar Cliente")
            print("4. Eliminar Cliente")
            print("5. Retornar al Menú Anterior")
            choice = input("Seleccione una opción: ")

            if choice == "1":
                print("Agregar Cliente Persona Jurídica seleccionado.")
                # Lógica para agregar cliente persona jurídica
            elif choice == "2":
                print("Buscar Cliente Persona Jurídica seleccionado.")
                # Lógica para buscar cliente persona jurídica
            elif choice == "3":
                print("Actualizar Cliente Persona Jurídica seleccionado.")
                # Lógica para actualizar cliente persona jurídica
            elif choice == "4":
                print("Eliminar Cliente Persona Jurídica seleccionado.")
                # Lógica para eliminar cliente persona jurídica
            elif choice == "5":
                print("Retornando al Menú de Cliente.")
                break
            else:
                print("Opción no válida. Intente de nuevo.")



# Ejecución del programa
if __name__ == "__main__":
    url = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/products.json"  # URL de ejemplo
    main_app = Main(url)
    main_app.LoadData()  # Cargar los datos y ejecutar el método DataStorage
    main_app.main_menu()
#Product.list_all_products()

   


