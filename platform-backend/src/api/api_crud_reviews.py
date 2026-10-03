from dynamoDB import setup
from dynamoDB.db_crud_reviews import DB_CRUD_REVIEWS
from model.entity.jsonencoders.review_encoder import ReviewEncoder
from model.entity.reviews.project_reviews import ProjectReviews
from model.entity.reviews.review import Review
from s3.s3_crud import S3_OPERATIONS
from utils.utils import Utils

from api.api_crud_projects import API_CRUD_PROJECTS


class API_CRUD_REVIEWS:
    def __init__(self, api_crud_projects: API_CRUD_PROJECTS):
        self.__db_crud_reviews = setup.startSetup('Reviews')
        self.__apiProj = api_crud_projects

    def getReview(self, idOfTheReview):
        return self.__db_crud_reviews.getReview(idOfTheReview)

    def addReview(self, reviewObj: Review):

        projJson = self.__apiProj.getProject(reviewObj.get_projectID())
        projJson2 = projJson

        projJson["projectReviews"]["reviews"].append(reviewObj.get_id())
        reviews = projJson["projectReviews"]
        reviews["average_rating"] = Utils.update_average_rating(reviews["average_rating"], reviews["total_reviews"], reviewObj.get_review_rating())
        reviews["total_reviews"] += 1

        self.__apiProj.updateProject(projJson2, projJson, None)

        return self.__db_crud_reviews.addReview(ReviewEncoder.toJson(reviewObj))

    def updateReview(self, reviewJson):
        # Swap the old rating for the new one in the project's average
        oldReview = self.__db_crud_reviews.getReview(reviewJson['id'])
        projJson = self.__apiProj.getProject(oldReview['projectID'])
        reviews = projJson["projectReviews"]
        reviews["average_rating"] = Utils.update_average_rating(reviews["average_rating"], reviews["total_reviews"], oldReview["review_rating"], -1)
        reviews["average_rating"] = Utils.update_average_rating(reviews["average_rating"], reviews["total_reviews"] - 1, reviewJson["review_rating"])
        self.__apiProj.updateProject(projJson, projJson, None)

        return self.__db_crud_reviews.updateReview(reviewJson)

    def deleteReview(self, idOfTheReview):

        # deleting the review id from project's review id list
        reviewJson = self.__db_crud_reviews.getReview(idOfTheReview)
        projJson = self.__apiProj.getProject(reviewJson['projectID'])
        projJson2 = projJson

        projectReviewsJson = projJson['projectReviews']
        projectReviewIdListJson = projectReviewsJson['reviews']
        projectReviewIdListJson.remove(idOfTheReview)

        projectReviewsJson["average_rating"] = Utils.update_average_rating(projectReviewsJson["average_rating"], projectReviewsJson["total_reviews"], reviewJson["review_rating"], -1)
        projectReviewsJson["total_reviews"] -= 1
        projectReviewsJson['reviews'] = projectReviewIdListJson
        projJson['projectReviews'] = projectReviewsJson

        self.__apiProj.updateProject(projJson2, projJson, None)

        return self.__db_crud_reviews.deleteReview(idOfTheReview)
