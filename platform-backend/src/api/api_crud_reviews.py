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


        # we add the review to the list of reviews
        # projectReviewsJson = projJson['projectReviews']
        # projectReviewIdListJson = projectReviewsJson['reviews']

        # if len(projectReviewIdListJson) == 0:  # change initial values to correct
        #     projectReviewsJson['total_reviews'] = "1"
            
        #     projectReviewsJson['average_rating'] = str(reviewObj.get_review_rating())
        # else:

        #     projectReviewsJson['total_reviews'] = str(int(projectReviewsJson['total_reviews']) + 1) 

        #     projectReview = ProjectReviews(projectReviewsJson['id'], int(projectReviewsJson['total_reviews']) + 1, 
        #                         int(projectReviewsJson['average_rating']), projectReviewsJson['reviews'])
        #     average_rating = ReviewUtils.average_review_calculator(self, projectReview)
        #     projectReviewsJson['average_rating'] = str(average_rating)
            
        # # aici bag modificarile in json-ul mare
        # projectReviewIdListJson.insert(0, reviewObj.get_id())

        # projectReviewsJson['reviews'] = projectReviewIdListJson
        # projJson['projectReviews'] = projectReviewsJson

        # self.__apiProj.updateProject(projJson2, projJson, None)

        return self.__db_crud_reviews.addReview(ReviewEncoder.toJson(reviewObj))

    def updateReview(self, reviewJson):
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
