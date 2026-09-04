import string


class Warning:
    def __init__(self, id: str, studentId: str, issuedBy: str, text: str, issuedDate):
        self.__id = id
        self.__studentId = studentId
        self.__issuedBy = issuedBy
        self.__text = text
        self.__issuedDate = issuedDate

    def get_id(self):
        return self.__id

    def get_studentId(self):
        return self.__studentId

    def get_issuedBy(self):
        return self.__issuedBy

    def get_text(self):
        return self.__text

    def set_text(self, text: string):
        self.__text = text

    def get_issuedDate(self):
        return self.__issuedDate
