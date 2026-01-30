#from config import SERVER_PORT

SERVER_PORT = 587


class ContactMail:

    def __init__(self, contact_mail, contact_password):
        self.__contact_mail = contact_mail
        self.__contact_password = contact_password
        self.__server_port = SERVER_PORT

    def get_contact_mail(self):
        return self.__contact_mail

    def get_contact_password(self):
        return self.__contact_password

    def get_server_port(self):
        return self.__server_port
