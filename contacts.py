class Contacts:
    def __init__ (self, adress="", mobile=0, nif=0, email=""):
        self.adress = adress
        self.mobile = mobile
        self.nif = nif
        self.email = email

    def set_adress (self, adress):
        self.adress = adress

    def set_mobile (self, mobile):
        self.mobile = mobile

    def set_nif (self, nif):
        self.nif = nif

    def set_email (self, email):
        self.email = email

    def get_adress (self):
        return self.adress

    def get_mobile (self):
        return self.mobile

    def get_nif (self):
        return self.nif

    def get_email (self):
        return self.email

    def search_by_query (self):
        if str(self.nif).startswith(query) or str(self.mobile).startswith(query):
            return True
        return False

    def to_dict (self):
        return {"adress":self.get_adress(), "mobile":self.get_mobile(),
                "nif":self.get_nif(), "email":self.get_email()}
