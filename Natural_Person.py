from Client import Client
import json

class Natural_Person(Client):
    file_name = "Natural_Person.json"

    def __init__(self, shipping_address=None, phone_number=None, email=None, name=None, last_name=None, identification=None):
        super().__init__(shipping_address, phone_number, email)
        self.name = name
        self.last_name = last_name
        self.identification = identification

    # Métodos CRUD específicos para Natural_Person
    @classmethod
    def create(cls, instance):
        """Guarda una instancia en el archivo JSON."""
        if not isinstance(instance, cls):
            raise TypeError("El argumento debe ser una instancia de Natural_Person.")
        # Leer los datos existentes
        data = cls.read_all()
        # Agregar la nueva persona
        data.append(instance.to_dict())
        # Escribir los datos actualizados
        cls._write(data)
        print("Natural Person created and saved successfully.")
        #def create(self, shipping_address, phone_number, email, name, last_name, identification):
        #    super().create(shipping_address, phone_number, email)
        #    self.name = name
        #    self.last_name = last_name
        #    self.identification = identification
        #    print("Natural Person created.")
        #@classmethod
        #def create(cls, instance: Client):
        #      """Crea un nuevo registro en el archivo correspondiente."""
        #    data = cls.read_all()
        #    data.append(instance.to_dict())  # Convierte la instancia en un diccionario
        #   cls._write(data)
    
    #def read(self):
    #    data = super().read()
    #    data.update({
    #
    #        "last_name": self.last_name,
    #        "identification": self.identification
    #    })
    #    return data


    def get_client(identifier: str, file_path: str):
        try:
            with open(file_path, 'r') as file:
                clients = json.load(file)
            for client in clients:
                if  client.get("identification") == identifier:
                    return client
            return None
        except FileNotFoundError:
            print("El archivo no existe.")
            return None

    #def update(self, shipping_address=None, phone_number=None, email=None, name=None, last_name=None, identification=None):
    #    super().update(shipping_address, phone_number, email)
    #    if name:
    #        self.name = name
    #    if last_name:
    #        self.last_name = last_name
    #    if identification:
    #        self.identification = identification
    #    print("Natural Person updated.")

    #def update(identifier: str, updated_client: 'Natural_Person', file_path: str):
    #    try:
    #        with open(file_path, 'r') as file:
    #            clients = json.load(file)

     #       updated = False
     #       for i, client in enumerate(clients):
    #            if client.get("identification") == identifier:
    ##                clients[i] = updated_client.to_dict()
     ##               updated = True
      #              break

#            if updated:
 #               with open(file_path, 'w') as file:
  #                  json.dump(clients, file, indent=4)
   #             print(f"Cliente con identificación '{identifier}' actualizado exitosamente.")
    #$        else:
    #            print(f"Cliente con identificación '{identifier}' no encontrado.")
      #  except FileNotFoundError:
       #     print("El archivo no existe.")

#
    @staticmethod
    def update(identifier: str, updated_data: dict, file_path: str):
        Client.update(identifier, updated_data, file_path)


    #def delete(self):
    #    super().delete()
    #    self.name = None
    #    self.last_name = None
   #     self.identification = None
    #    print("Natural Person deleted.")
    @staticmethod
    def delete_client(identifier: str, file_path: str):
        Client.delete_client(identifier, file_path)

    def to_dict(self):
        """Convierte el objeto en un diccionario."""
        return {
            "shipping_address": self.shipping_address,
            "phone_number": self.phone_number,
            "email": self.email,
            "identification": self.identification,
            "name": self.name,
            "last_name": self.last_name
        }   
    

    #Prueba 

    
