class Review:
    def __init__(self, id: str, userID: str, projectID: str, review_description: str, review_rating: float):
        self.__id = id
        self.__userID = userID
        self.__projectID = projectID
        self.__review_description = review_description
        self.__review_rating = review_rating

    def get_id(self):
        return self.__id
    def set_id(self, id):
        self.__id = id

    def get_userId(self):
        return self.__userID
    def set_userId(self, userID):
        self.__userID = userID

    def get_projectID(self):
        return self.__projectID
    def set_projectID(self, projectID):
        self.__projectID = projectID

    def get_review_description(self):
        return self.__review_description
    def set_review_description(self, review_description):
        self.__review_description = review_description

    def get_review_rating(self):
        return self.__review_rating
    def set_review_rating(self, review_rating):
        self.__review_rating = review_rating
