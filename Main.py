import requests 
import os
import json
from Product import Product  # Asegúrate de que Product.py esté en el mismo directorio o en el path
from Client import Client
from Natural_Person import Natural_Person
from Legal_Entity import Legal_Entity
from Shipping import Shipping, Shipping_Service, Shipping_Method, Shipping_Status
from Payment import Payment, Payment_Method, Payment_Status, Currency
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
            print("1. Gestión de Productos")
            print("2. Gestión de Clientes")
            print("3. Gestión de Ventas")
            print("4. Gestión de Pagos")
            print("5. Gestión de Envios")
            print("6. Gestión de Indicadores")
            print("7. Salir")
            choice = input("Seleccione una opción: ")

            if choice == "1":
                self.product_menu()
            elif choice == "2":
                self.client_menu()
            elif choice == "3":
                self.ventas()
            elif choice == "4":
                self.pagos()
            elif choice == "5":
                self.envios()
            elif choice == "6":
                self.indicadores()    
            elif choice == "7":
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
                self.agregar_cliente_juridico()
            elif choice == "2":
                print("Buscar Cliente Persona Jurídica seleccionado.")
                self.buscar_persona_juridica()
            elif choice == "3":
                print("Actualizar Cliente Persona Jurídica seleccionado.")
                self.modificar_persona_juridica()
            elif choice == "4":
                print("Eliminar Cliente Persona Jurídica seleccionado.")
                self.eliminar_persona_juridica()
            elif choice == "5":
                print("Retornando al Menú de Cliente.")
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    def agregar_cliente_juridico(self):
        natural_file = "Natural_Person.json"
        rif = input("RIF: ")
        if Legal_Entity.read(rif):
            print("El rif esta previamente registrado, por favor indicar un rif diferente.")
            input("Presione cualquier tecla para continuar...")
        else:
            company_name = input("Nombre de la compañía: ")
            phone_number = input("Número de teléfono de la compañía: ")
            company_email = input("Correo electrónico de la compañía: ")
            shipping_address = input("Dirección de envio de la compañía: ")
            while True:
                contact_identification = input("Cédula de la persona de contacto: ")
                client = Natural_Person.get_client(contact_identification, natural_file)
                if client:
                    print()
                    print(f"Nombre: {client['name']}")
                    print(f"Apellido: {client['last_name']}")
                    print(f"Correo-e: {client['email']}")
                    print(f"Número de Teléfono: {client['phone_number']}")
                    print(f"Direccion de envio: {client['shipping_address']}")
                    desicion = input("Desea asociar a esta persona como contacto S/N? ").capitalize()
                    if desicion == "S":
                        Legal_Entity.create(rif, company_name, contact_identification, shipping_address, phone_number, company_email)
                        input("Presione cualquier tecla para continuar...")
                        break
                    else:
                        continuar = input("Desea continuar en el proceso de registro S/N?: ").capitalize()
                        if continuar == 'N':
                            break
                        elif continuar == "S":
                            contact_identification = ""
                else:
                    print("Cliente no encontrado.")
                    contact_identification = ""
                    input("Presione cualquier tecla para continuar...")

    def buscar_persona_juridica(self):
        natural_file = "Natural_Person.json"
        rif = input("RIF: ")
        compania_leida = Legal_Entity.read(rif)
        if compania_leida:
            print()
            print(f"Nombre de la compañía: {compania_leida['company_name']}")
            print(f"Numero de telefono de la compañía: {compania_leida['phone_number']}")
            print(f"Dirección de envio de la compañía: {compania_leida['shipping_address']}")
            print(f"Correo electronico de la compañía: {compania_leida['email']}")
            print(f"Numero de cédula de la persona de contacto: {compania_leida['contactPersonIdentification']}")
            client = Natural_Person.get_client(compania_leida['contactPersonIdentification'], natural_file)
            if client:
                    print(f"Nombre: {client['name']}")
                    print(f"Apellido: {client['last_name']}")
                    print(f"Correo-e: {client['email']}")
                    print(f"Número de Teléfono: {client['phone_number']}")
                    print(f"Direccion de envio: {client['shipping_address']}")
            else:
                    print("Cliente no encontrado, revise en el modulo de cliente que el número de cédula este registrado.")
            input("Presione cualquier tecla para continuar...")
        else:
            print("Cliente juridico no encontrado.")
            input("Presione cualquier tecla para continuar...")

    def modificar_persona_juridica(self):
        natural_file = "Natural_Person.json"
        rif = input("RIF: ")
        compania_leida = Legal_Entity.read(rif)
        if compania_leida:
            print("Ingrese los nuevos datos (deje en blanco para mantener el actual):")
            new_company_name = input(f"Nuevo nombre de la compañía ({compania_leida['company_name']}): ") or compania_leida['company_name']
            new_phone_number = input(f"Nuevo número de telefono de la compañía: ({compania_leida['phone_number']}): ") or compania_leida['phone_number']
            new_shipping_address = input(f"Nueva dirección de envio de la compañía: ({compania_leida['shipping_address']}): ") or compania_leida['shipping_address']
            new_email = input(f"Nuevo correo electronico de la compañía: ({compania_leida['email']}): ") or compania_leida['email']
            while True:
                new_contact_person_identification = input(f"Actualización de contacto de la compañía: ({compania_leida['contactPersonIdentification']}): ") or compania_leida['contactPersonIdentification']
                # new_contact_person_identification = input("Cédula de la persona de contacto: ")
                client = Natural_Person.get_client(new_contact_person_identification, natural_file)
                if client:
                    print(f"Nombre: {client['name']}")
                    print(f"Apellido: {client['last_name']}")
                    print(f"Correo-e: {client['email']}")
                    print(f"Número de Teléfono: {client['phone_number']}")
                    print(f"Direccion de envio: {client['shipping_address']}")
                    desicion = input("Desea asociar a esta persona como contacto S/N? ").capitalize()
                    if desicion == "S":
                        updated_data = {
                            "company_name": new_company_name,
                            "phone_number": new_phone_number,
                            "shipping_address": new_shipping_address,
                            "email": new_email,
                            "contactPersonIdentification": new_contact_person_identification}
                        Legal_Entity.update(rif, updated_data)
                        # Legal_Entity.update(rif, {"company_name": new_company_name, "phone_number": new_phone_number, "shipping_address": new_shipping_address, "email": new_email, 'contactPersonIdentification': new_contact_person_identification})
                        input("Presione cualquier tecla para continuar...")
                        break
                    else:
                        continuar = input("Desea continuar en el proceso de actualización de los datos de la persona juridica? (S/N): ").capitalize()
                        if continuar == 'N':
                            break
                        elif continuar == "S":
                            contact_identification = ""
                else:
                    print("Cliente no encontrado.")
                    contact_identification = ""
                    input("Presione cualquier tecla para continuar...")
        else:
            print("Cliente juridico no encontrado.")
            input("Presione cualquier tecla para continuar...")

    def eliminar_persona_juridica(self):
        natural_file = "Natural_Person.json"
        rif = input("RIF: ")
        compania_leida = Legal_Entity.read(rif)
        if compania_leida:
            decision = input(f"Esta seguro que desea eliminar el cliente {compania_leida['company_name']} (Y/N)?: ").capitalize()
            if decision == 'Y':
                Legal_Entity.delete(rif)
        else:
            print("Cliente juridico no encontrado.")
            input("Presione cualquier tecla para continuar...")

    def ventas(self):
        while True:
            self.clear_terminal()
            print("\n--- Modulo de Ventas ---")
            print("1. Registrar Venta")
            print("2. Buscar Ventas")
            print("3. Obtener Cantidad de Productos ")
            print("4. Retornar al Menú Anterior")
            choice = input("Seleccione una opción: ")

            if choice == "1":
                self.registrar_ventas()
            elif choice == "2":
                print("Buscar Ventas.")
                # Lógica para buscar cliente persona jurídica
            elif choice == "3":
                print("Obtener Cantidad de Productos.")
                # Lógica para actualizar cliente persona jurídica
            elif choice == "4":
                print("Retornando al Menú anterior.")
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    def registrar_ventas(self):
        self.clear_terminal()
        print("---Modulo de ventas--- \nSeleccione el tipo de cliente: \n1. Cliente natural \n2. Cliente Juridico")
        seleccion = input("---> ")

        if seleccion == '1':
            identificacion = self.menu_buscar_cliente_natural()
            print(f"Valor de identificacion: {identificacion}")
            if identificacion:
                producto_sel = self.menu_buscar_producto()
                cantidad = int(input("Indique la cantidad del producto elegido a comprar: "))
                pago_por_envio =  self.registro_venta_envio()
                envio_id = Shipping.get_next_shipping_id() - 1
                print(f"El pago por producto del id {producto_sel['product_id']} con precio {producto_sel['price']}") 
                print(f"El pago por envio es {pago_por_envio}")
                subtotal_producto = producto_sel["price"] * cantidad
                monto_a_pagar = self.registrar_pago_venta(subtotal_producto, pago_por_envio)
                print(monto_a_pagar)
                # pago_id = Payment.get_next_payment_id() - 1
                # print(f"El número de referencia de pago es: {pago_id}")
                input("Presione cualquier tecla para continuar...")
                
            else:
                print("No entre")
                input("Presione cualquier tecla para continuar...")
            

        elif seleccion == '2':
            pass
        elif seleccion == '3':
            pass
        
    def pagos(self):
        while True:
            self.clear_terminal()
            print("\n--- Modulo de Pagos ---")
            print("1. Registrar pagos")
            print("2. Buscar pagos")
            print("3. Retornar al Menú Anterior")
            menu = input("---> ")

            if menu == '1':
                self.registrar_pagos()
            elif menu == '2':
                self.buscar_pagos()
            elif menu == '3':
                break

    def registrar_pagos(self):
        amount = float(input("Monto del pago: "))
        precio_producto = 1
        precio_envio = 2
        self.registrar_pago_venta(precio_producto, precio_envio)
        print("Pago agregado exitosamente.")
        input("Presione cualquier tecla para continuar...")

    def buscar_pagos(self):
        payment_file = "Payment.json"
        print("Buscar numero de pago.")
        identification_payment = int(input("Número de pago: "))
                #print(Natural_Person.read(identification , natural_file))
                #input("Presione cualquier tecla para continuar...")
        payment_leido = Payment.get_payment(identification_payment)
        #if shipping_leido:
            #print(f"Envío encontrado: {shipping_leido}")
        #else:
            # print("Envío no encontrado.")
        # cliente_Leido= Natural_Person.get_client(identification , shipping_file)
        if payment_leido:
            self.clear_terminal()
            print("Envio encontrado:")
            print(f"Identificacion del pago: {payment_leido["paymentId"]}")
            print(f"Monto del pago: {payment_leido['amount']}")
            print(f"Moneda de pago: {payment_leido['currency']}")
            print(f"Metodo de pago: {payment_leido['method']}")
            print(f"Estatus del pago: {payment_leido['status']}")
            print(f"Fecha del pago: {payment_leido['date']}")

        else:
            print("Pago no encontrado.")
        input("Presione cualquier tecla para continuar...")

    def envios(self):
        while True:
            self.clear_terminal()
            print("\n--- Modulo de Envios ---")
            print("1. Registrar envios")
            print("2. Buscar envios")
            print("3. Retornar al Menú Anterior")
            menu = input("---> ")

            if menu == '1':
                self.registrar_envios()
            elif menu == '2':
                self.buscar_envios()
            elif menu == '3':
                break

    def registrar_envios(self):
        self.clear_terminal()
        self.registro_venta_envio()
        input("Presione cualquier tecla para continuar...")

    def buscar_envios(self):
        shipping_file = "Shipping.json"
        print("Buscar envio seleccionado.")
        identification_shipping = int(input("Número de envio: "))
                #print(Natural_Person.read(identification , natural_file))
                #input("Presione cualquier tecla para continuar...")
        shipping_leido = Shipping.get_shipping(identification_shipping)
        #if shipping_leido:
            #print(f"Envío encontrado: {shipping_leido}")
        #else:
            # print("Envío no encontrado.")
        # cliente_Leido= Natural_Person.get_client(identification , shipping_file)
        if shipping_leido:
            self.clear_terminal()
            print("Envio encontrado:")
            print(f"Identificacion del envio: {shipping_leido["shippingId"]}")
            print(f"Empresa de envios: {shipping_leido['shipping_service']}")
            print(f"Metodo de envio: {shipping_leido['shipping_method']}")
            print(f"Estatus del envio: {shipping_leido['shipping_status']}")
            print(f"Precio del servicio: {shipping_leido['service_price']}")

        else:
            print("Envio no encontrado.")
        input("Presione cualquier tecla para continuar...")

    def menu_buscar_cliente_natural(self):
        natural_file = "Natural_Person.json"
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
            input("Presione cualquier tecla para continuar...")
            return cliente_Leido['identification']
        else:
            print("Cliente no encontrado.")
            input("Presione cualquier tecla para continuar...")
            return False
        
    def menu_buscar_producto(self):
        Product.list_all_products()
        eleccion = int(input("Seleccione el id del producto que va a comprar: "))
        producto = Product.get_product(eleccion)
        product_price = producto['price']
        producto_seleccionado = {'product_id': eleccion, 'price': product_price}
        return producto_seleccionado # Elección representa el Id del producto a comprar
    
    def registro_venta_envio(self):
        print("Servicio de envios: \n1. MRW \n2. Tealca \n3. Ipostel")
        shipping_service = input("---> ")
        while True:
            if shipping_service == '1':
                servicio_seleccionado = Shipping_Service.MRW
                break
            elif shipping_service == '2':
                servicio_seleccionado = Shipping_Service.Tealca
                break
            elif shipping_service == '3':
                servicio_seleccionado = Shipping_Service.Ipostel
                break
            else:
                print("Ha ingresado un valor incorrecto, por favor indique uno de los valores seleccionados")
        print("Método de envios: \n1. Oficina de retiro \n2. Puerta a Puerta \n3. Apartado postal")
        shipping_method = input("---> ")
        while True:
            if shipping_method == '1':
                metodo_seleccionado = Shipping_Method.Oficina_de_retiro
                break
            elif shipping_method == '2':
                metodo_seleccionado = Shipping_Method.Puerta_a_Puerta
                break
            elif shipping_method == '3':
                metodo_seleccionado = Shipping_Method.Apartado_postal
                break
            else:
                print("Ha ingresado un valor incorrecto, por favor indique uno de los valores seleccionados")
        service_price = float(input("Precio del envio: "))
        status = "Procesado"

        # Ejemplo de cómo crear un envío y guardarlo
        new_shipping = Shipping(servicio_seleccionado, metodo_seleccionado, Shipping_Status.Procesado, service_price)
        new_shipping.create_shipping()
        return service_price

        # Llamar al método create para guardar la instancia
        print("Envio agregado exitosamente.")

    def registrar_pago_venta(self, precio_producto: float, precio_envio: float) -> float:
        
        print("Moneda de pago: \n1. Dolar estadounidense \n2. Bolivar \n3. Euro \n4. Libra esterlina \n5. Franco suizo \n6. Yuan chino")
        currency = input("---> ")
        while True:
            if currency == '1':
                moneda_seleccionada = Currency.USD
                break
            elif currency == '2':
                moneda_seleccionada = Currency.VEF
                break
            elif currency == '3':
                moneda_seleccionada = Currency.EUR
                break
            elif currency == '4':
                moneda_seleccionada = Currency.GBP
                break
            elif currency == '5':
                moneda_seleccionada = Currency.CHF
                break
            elif currency == '6':
                moneda_seleccionada = Currency.CNY
                break
            else:
                print("Ha ingresado una moneda invalida, por favor indique uno de los valores seleccionados")
        print("Metodo de pago: \n1. Punto de venta \n2. Pago movil \n3. Transferencia \n4. Zelle \n5. PayPal \n6. Efectivo")
        payment_method = input("---> ")
        while True:
            if payment_method == '1':
                metodo_seleccionado = Payment_Method.POS
                break
            elif payment_method == '2':
                metodo_seleccionado = Payment_Method.MOBILE
                break
            elif payment_method == '3':
                metodo_seleccionado = Payment_Method.TRANSFER
                break
            elif payment_method == '4':
                metodo_seleccionado = Payment_Method.ZELLE
                break
            elif payment_method == '5':
                metodo_seleccionado = Payment_Method.PAYPAL
                break
            elif payment_method == '6':
                metodo_seleccionado = Payment_Method.CASH
                break
            else:
                print("Ha ingresado un metodo invalido, por favor indique uno de los valores seleccionados")
        status = Payment_Status.PROCESSING

        # Ejemplo de cómo crear un envío y guardarlo
        amount = precio_producto + precio_envio
        new_payment = Payment.create_payment(amount, moneda_seleccionada, metodo_seleccionado, status)
        print(f"El valor a pagar es: {amount}")
        return amount # Se retorna la cantidad a pagar

        # Llamar al método create para guardar la instancia


# Ejecución del programa
if __name__ == "__main__":
    url = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/products.json"  # URL de ejemplo
    main_app = Main(url)
    main_app.LoadData()  # Cargar los datos y ejecutar el método DataStorage
    main_app.main_menu()
#Product.list_all_products()


