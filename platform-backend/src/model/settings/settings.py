class Settings():
    def __init__(self, language: str, notifications: bool, theme: bool):
        
        self.__language = language
        self.__notifications = notifications
        self.__theme = theme

    def get_language(self):
        return self.__language
        
    def set_language(self, new_language: bool):
        self.__language = new_language
    
    def get_notifications(self):
        return self.__notifications

    def set_notifications(self, new_notifications: bool):
        self.__notifications = new_notifications

    def get_theme(self):
        return self.__theme
        
    def set_theme(self, new_theme: bool):
        self.__theme = new_theme
