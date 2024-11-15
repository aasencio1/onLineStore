class Person:
    def __init__(self, shipping_address=None, phone_number=None, email=None):
        self.shipping_address = shipping_address
        self.phone_number = phone_number
        self.email = email

    # Métodos CRUD para la clase base Person
    def create(self, shipping_address, phone_number, email):
        self.shipping_address = shipping_address
        self.phone_number = phone_number
        self.email = email
        print("Person created.")

    def read(self):
        return {
            "shipping_address": self.shipping_address,
            "phone_number": self.phone_number,
            "email": self.email
        }

    def update(self, shipping_address=None, phone_number=None, email=None):
        if shipping_address:
            self.shipping_address = shipping_address
        if phone_number:
            self.phone_number = phone_number
        if email:
            self.email = email
        print("Person updated.")

    def delete(self):
        self.shipping_address = None
        self.phone_number = None
        self.email = None
        print("Person deleted.")


class Legal_Entity(Person):
    def __init__(self, shipping_address=None, phone_number=None, email=None, company_name=None, rif=None, contact_person=None):
        super().__init__(shipping_address, phone_number, email)
        self.company_name = company_name
        self.rif = rif
        self.contact_person = contact_person  # contact_person es una instancia de Natural_Person

    # Métodos CRUD específicos para Legal_Entity
    def create(self, shipping_address, phone_number, email, company_name, rif, contact_person):
        super().create(shipping_address, phone_number, email)
        self.company_name = company_name
        self.rif = rif
        self.contact_person = contact_person
        print("Legal Entity created.")

    def read(self):
        data = super().read()
        data.update({
            "company_name": self.company_name,
            "rif": self.rif,
            "contact_person": self.contact_person.read() if self.contact_person else None
        })
        return data

    def update(self, shipping_address=None, phone_number=None, email=None, company_name=None, rif=None, contact_person=None):
        super().update(shipping_address, phone_number, email)
        if company_name:
            self.company_name = company_name
        if rif:
            self.rif = rif
        if contact_person:
            self.contact_person = contact_person
        print("Legal Entity updated.")

    def delete(self):
        super().delete()
        self.company_name = None
        self.rif = None
        self.contact_person = None
        print("Legal Entity deleted.")


class Natural_Person(Person):
    def __init__(self, shipping_address=None, phone_number=None, email=None, name=None, last_name=None, identification=None):
        super().__init__(shipping_address, phone_number, email)
        self.name = name
        self.last_name = last_name
        self.identification = identification

    # Métodos CRUD específicos para Natural_Person
    def create(self, shipping_address, phone_number, email, name, last_name, identification):
        super().create(shipping_address, phone_number, email)
        self.name = name
        self.last_name = last_name
        self.identification = identification
        print("Natural Person created.")

    def read(self):
        data = super().read()
        data.update({
            "name": self.name,
            "last_name": self.last_name,
            "identification": self.identification
        })
        return data

    def update(self, shipping_address=None, phone_number=None, email=None, name=None, last_name=None, identification=None):
        super().update(shipping_address, phone_number, email)
        if name:
            self.name = name
        if last_name:
            self.last_name = last_name
        if identification:
            self.identification = identification
        print("Natural Person updated.")

    def delete(self):
        super().delete()
        self.name = None
        self.last_name = None
        self.identification = None
        print("Natural Person deleted.")
