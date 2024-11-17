
from Client import Client

class Legal_Entity(Client):
    file_name = "Legal_Entity.json"  # Archivo específico para Legal_Entity

    def __init__(self, rif: str, company_name: str, contactPersonIdentification: str, 
        shipping_address: str, phone_number: str, email: str):
        super().__init__(shipping_address, phone_number, email)
        self.rif = rif
        self.company_name = company_name
        self.contactPersonIdentification = contactPersonIdentification

    def to_dict(self):
        """Convierte los atributos del objeto en un diccionario."""
        return {
            "rif": self.rif,
            "company_name": self.company_name,
            "contactPersonIdentification": self.contactPersonIdentification,
            "shipping_address": self.shipping_address,
            "phone_number": self.phone_number,
            "email": self.email
        }

    @classmethod
    def create(cls, rif, company_name, contactPersonIdentification, 
        shipping_address, phone_number, email):
        """Crea un nuevo registro en el archivo Legal_Entity.json."""
        instance = cls(rif, company_name, contactPersonIdentification, shipping_address, phone_number, email)
        data = cls.read_all()
        data.append(instance.to_dict())
        cls._write(data)
        print(f"Registro creado exitosamente para RIF: {rif}")

    @classmethod
    def read(cls, rif):
        """Busca una entidad jurídica por su RIF."""
        data = cls.read_all()
        for record in data:
            if record.get("rif") == rif:
                return record
        print(f"No se encontró ninguna entidad jurídica con el RIF: {rif}")
        return None

    @classmethod
    def update(cls, rif, updated_data):
        """Actualiza un registro basado en su RIF."""
        data = cls.read_all()
        for record in data:
            if record["rif"] == rif:
                record.update(updated_data)
                cls._write(data)
                print(f"Registro actualizado para RIF: {rif}")
                return
        print(f"No se encontró ninguna entidad jurídica con el RIF: {rif}")

    @classmethod
    def delete(cls, rif: str):
    # Elimina una entidad legal por su RIF."""
        data = cls.read_all()
        new_data = [entity for entity in data if entity['rif'] != rif]
        
        if len(new_data) == len(data):
            # Si la longitud no cambió, significa que el RIF no fue encontrado
            print(f"No se encontró la compañía con RIF '{rif}'.")
        else:
            # Si la longitud cambió, significa que se eliminó un registro
            cls._write(new_data)
            print(f"Compañía con RIF '{rif}' eliminada exitosamente.")


# Ejemplos de uso
"""
if __name__ == "__main__":
    # Crear un registro
    Legal_Entity.create(
        rif="J-12345678-9",
        company_name="Empresa Ejemplo S.A.",
        contactPersonIdentification="V-12345678",
        shipping_address="Calle Principal, Ciudad",
        phone_number="0414-1234567",
        email="empresa@ejemplo.com"
    )
"""

# Leer el registro
# print(Legal_Entity.read("J-12345678-9"))

    # Actualizar el registro
#Legal_Entity.update("J-12345678-9", {
#       "company_name": "Empresa Actualizada S.A.",
#      "email": "nuevo_email@ejemplo.com"
# })

    # Leer nuevamente para verificar los cambios
# print(Legal_Entity.read("J-12345678-9"))

    # Eliminar el registro
Legal_Entity.delete("J-12345678-9")

    # Intentar leer el registro eliminado
# print(Legal_Entity.read("J-12345678-9"))