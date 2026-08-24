from model.entity.reviews.project_reviews import ProjectReviews


class ReviewUtils:

    def __init__(self):
        pass

    @staticmethod
    def get_average_rating(new_rating: float, old_rating: float):
        return new_rating if old_rating == 0 else (old_rating + new_rating) / 2
