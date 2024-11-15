import json
from abc import ABC, abstractmethod

class Client(ABC):
    file_name = None  # Cada clase hija definirá su propio archivo JSON

    def __init__(self, shipping_address: str, phone_number: str, email: str):
        self.shipping_address = shipping_address
        self.phone_number = phone_number
        self.email = email

    @abstractmethod
    def to_dict(self):
        """Convierte los atributos del objeto en un diccionario."""
        pass

    @classmethod
    def create(cls, instance):
        """Crea un nuevo registro en el archivo correspondiente."""
        data = cls.read_all()
        data.append(instance.to_dict())
        cls._write(data)

    @classmethod
    def read_all(cls):
        """Lee todos los registros del archivo correspondiente."""
        try:
            with open(cls.file_name, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    #@classmethod
   # def update(cls, identifier, updated_instance):
    #    """Actualiza un registro en el archivo correspondiente."""
    #    data = cls.read_all()
     #   for index, record in enumerate(data):
      #      if record[identifier] == getattr(updated_instance, identifier):
       #         data[index] = updated_instance.to_dict()
       #         break
       # cls._write(data)
    @staticmethod
    def update(identifier: str, updated_data: dict, file_path: str):
        try:
            with open(file_path, 'r') as file:
                clients = json.load(file)
            
            updated = False
            for i, client in enumerate(clients):
                if client.get("identification") == identifier:
                    # Actualiza directamente el cliente con los nuevos datos
                    clients[i].update(updated_data)
                    updated = True
                    break
            
            if updated:
                with open(file_path, 'w') as file:
                    json.dump(clients, file, indent=4)
                print(f"Cliente con identificación '{identifier}' actualizado correctamente.")
            else:
                print(f"Cliente con identificación '{identifier}' no encontrado.")
        except FileNotFoundError:
            print("El archivo no existe.")

   # @classmethod
   # def delete(cls, identifier, value):
   #     """Elimina un registro del archivo correspondiente."""
   #     data = cls.read_all()
   #     data = [record for record in data if record[identifier] != value]
   #     cls._write(data)
    @staticmethod
    def delete_client(identifier: str, file_path: str):
        try:
            with open(file_path, 'r') as file:
                clients = json.load(file)

            # Filtrar los clientes que no coincidan con el identificador
            original_count = len(clients)
            clients = [client for client in clients if client.get("identification") != identifier]

            if len(clients) < original_count:
                # Guardar la lista actualizada en el archivo
                with open(file_path, 'w') as file:
                    json.dump(clients, file, indent=4)
                print(f"Cliente con identificación '{identifier}' eliminado correctamente.")
            else:
                print(f"Cliente con identificación '{identifier}' no encontrado.")
        except FileNotFoundError:
            print("El archivo no existe.")
        except Exception as e:
            print(f"Ocurrió un error al eliminar el cliente: {e}")
            
    @classmethod
    def _write(cls, data):
        """Escribe los datos en el archivo correspondiente."""
        with open(cls.file_name, "w") as file:
            json.dump(data, file, indent=4)

