import json
import os

class Product:
    products = []  # Lista para almacenar productos en memoria

    def __init__(self, data=None):
        # Si `data` es una lista de productos en formato JSON, cargar directamente
        self.data = data
        if data is not None:
            if isinstance(data, list):
                for item in data:
                    # Validar y crear productos individuales
                    try:
                        product = {
                            'product_id': int(item.get('id')),
                            'name': str(item.get('name')),
                            'description': str(item.get('description')),
                            'price': float(item.get('price')),
                            'category': str(item.get('category')),
                            'inventory': int(item.get('inventory')),
                            'compatible_vehicles': list(item.get('compatible_vehicles'))
                        }
                        self.products.append(product)
                    except (TypeError, ValueError) as e:
                        print(f"Error al procesar el producto: {e}")
                print("Productos cargados exitosamente en memoria.")
            else:
                print("Datos inválidos: se esperaba una lista de productos.")
    




    @staticmethod
    def esperar_continuar():
        input("Presione cualquier tecla para continuar...")

    # Método para almacenar productos en un archivo JSON
    def DataStorage(self):
        if self.data is not None:
            try:
                with open('data.json', 'w') as file:
                    json.dump(self.data, file, indent=4)
                print("Data has been stored in 'data.json'")
            except IOError as e:
                print(f"An error occurred while saving the file: {e}")
        else:
            print("No data to store.")


    # Método para crear un nuevo producto con validación de ID
    @classmethod
    def create_product(cls, product_data):
        # Verificar si el producto ya existe en la lista
        for product in cls.products:
            if product['product_id'] == product_data['product_id']:
                print("El Identificador del producto existe, favor ingrese un número diferente.")
                cls.esperar_continuar()
                return
        
        # Si el producto no existe, agregarlo a la lista
        cls.products.append(product_data)
        #print(f"Producto '{product_data['name']}' agregado exitosamente.")
        
        # Almacenar productos actualizados en el archivo JSON
        try:
            with open('data.json', 'w') as file:
                json.dump(cls.products, file, indent=4)
                print(f"Producto '{product_data['name']}' agregado exitosamente.")
            #print("Archivo 'data.json' actualizado exitosamente.")
        except IOError as e:
            print(f"Ocurrió un error al actualizar el archivo: {e}")
        
        cls.esperar_continuar()

    # Método para leer un producto por ID
    @classmethod
    def get_product(cls, product_id):
        for product in cls.products:
            # Asegurarse de que 'product_id' esté en el producto antes de acceder a él
            if 'product_id' in product and product['product_id'] == product_id:
                cls.esperar_continuar()
                return product
        print("Id del producto no existe, favor ingrese un número diferente.")
        cls.esperar_continuar()
        return None


    # Método para actualizar un producto por ID
    @classmethod
    def update_product(cls, product_id, **kwargs):
        # Buscar el producto en la lista
        for product in cls.products:
            if product['product_id'] == product_id:
                # Actualizar los valores proporcionados
                for key, value in kwargs.items():
                    if key in product:
                        product[key] = value
                print(f"Producto con ID '{product_id}' actualizado exitosamente.")
                
                # Guardar los cambios en el archivo JSON
                try:
                    with open('data.json', 'w') as file:
                        json.dump(cls.products, file, indent=4)
                    print("Archivo 'data.json' actualizado después de la actualización.")
                except IOError as e:
                    print(f"Ocurrió un error al actualizar el archivo: {e}")
                
                cls.esperar_continuar()
                return
        
        # Si no se encuentra el producto, mostrar mensaje de error
        print("Id del producto no existe, favor ingrese un número diferente.")
        cls.esperar_continuar()

    # Método para eliminar un producto por ID
    @classmethod
    def delete_product(cls, product_id):
        for product in cls.products:
            if product['product_id'] == product_id:
                cls.products.remove(product)
                print(f"Producto con ID '{product_id}' eliminado exitosamente.")
                
                # Actualizar el archivo JSON
                try:
                    with open('data.json', 'w') as file:
                        json.dump(cls.products, file, indent=4)
                    print("Archivo 'data.json' actualizado después de eliminar el producto.")
                except IOError as e:
                    print(f"Ocurrió un error al actualizar el archivo: {e}")
                
                cls.esperar_continuar()
                return
        
        # Si el producto no se encuentra, mostrar mensaje de error
        print("Id del producto no existe, favor ingrese un número diferente.")
        cls.esperar_continuar() 

    @classmethod
    def list_all_products(cls):
        if cls.products:
            for product in cls.products:
                print(f"ID: {product['product_id']}, Name: {product['name']}, Description: {product['description']}, "
                      f"Price: {product['price']}, Category: {product['category']}, Inventory: {product['inventory']}, "
                      f"Compatible Vehicles: {', '.join(product['compatible_vehicles'])}")
        else:
            print("No hay productos disponibles.")