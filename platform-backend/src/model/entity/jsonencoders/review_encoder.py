from model.entity.reviews.review import Review


class ReviewEncoder:
    def toJson(review):
        if isinstance(review, Review):
            newItem = {
                'id': review.get_id(),
                'userID': review.get_userId(),
                'projectID': review.get_projectID(),
                'review_description': review.get_review_description(),
                'review_rating': review.get_review_rating()
            }
            return newItem
        return None
