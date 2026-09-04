import string


class Challenge:
    def __init__(self, id: str, name: str, description: str, deadline: str, maxScore, createdBy: str, creationDate):
        self.__id = id
        self.__name = name
        self.__description = description
        self.__deadline = deadline
        self.__maxScore = maxScore
        self.__createdBy = createdBy
        self.__creationDate = creationDate

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def set_name(self, name: string):
        self.__name = name

    def get_description(self):
        return self.__description

    def set_description(self, description: string):
        self.__description = description

    def get_deadline(self):
        return self.__deadline

    def set_deadline(self, deadline: string):
        self.__deadline = deadline

    def get_maxScore(self):
        return self.__maxScore

    def set_maxScore(self, maxScore):
        self.__maxScore = maxScore

    def get_createdBy(self):
        return self.__createdBy

    def get_creationDate(self):
        return self.__creationDate
