class Award:
    def __init__(self, id: str, name: str, userId: str, description: str, imageId: str):
        self.__id = id
        self.__name = name
        self.__userId = userId
        self.__description = description
        self.__imageId = imageId

    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_userId(self):
        return self.__userId

    def set_userId(self, userId):
        self.__userId = userId

    def get_description(self):
        return self.__description

    def set_description(self, description):
        self.__description = description

    def get_imageId(self):
        return self.__imageId

    def set_imageId(self, imageId):
        self.__imageId = imageId
