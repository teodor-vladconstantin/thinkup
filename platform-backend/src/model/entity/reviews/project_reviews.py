class ProjectReviews:
    def __init__(self, id: str, total_review: int, average_rating: float, reviews: list):
        self.__id = id
        self.__total_reviews = total_review
        self.__average_rating = average_rating
        self.__reviews = reviews

    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id

    def get_total_reviews(self):
        return self.__total_reviews

    def set_total_reviews(self, total_reviews):
        self.__total_reviews = total_reviews

    def get_average_rating(self):
        return self.__average_rating

    def set_average_rating(self, average_rating):
        self.__average_rating = average_rating

    def get_reviews(self):
        return self.__reviews

    def set_reviews(self, reviews):
        self.__reviews = reviews
