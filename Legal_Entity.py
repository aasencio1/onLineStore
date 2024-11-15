from Client import Client

class Legal_Entity(Client):
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



