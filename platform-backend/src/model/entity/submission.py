import string


class Submission:
    def __init__(self, id: str, studentId: str, challengeId: str, score, gradedBy: str, gradedDate, feedback: string = None):
        self.__id = id
        self.__studentId = studentId
        self.__challengeId = challengeId
        self.__score = score
        self.__gradedBy = gradedBy
        self.__gradedDate = gradedDate
        self.__feedback = feedback

    def get_id(self):
        return self.__id

    def get_studentId(self):
        return self.__studentId

    def get_challengeId(self):
        return self.__challengeId

    def get_score(self):
        return self.__score

    def set_score(self, score):
        self.__score = score

    def get_gradedBy(self):
        return self.__gradedBy

    def set_gradedBy(self, gradedBy: string):
        self.__gradedBy = gradedBy

    def get_gradedDate(self):
        return self.__gradedDate

    def set_gradedDate(self, gradedDate):
        self.__gradedDate = gradedDate

    def get_feedback(self):
        return self.__feedback

    def set_feedback(self, feedback: string):
        self.__feedback = feedback
