from api.api_crud_projects import API_CRUD_PROJECTS
from api.api_crud_reviews import API_CRUD_REVIEWS
from api.api_track_activity import updateActivity
from dynamoDB import setup
from flask import Blueprint, request
from model.entity.reviews.review import Review

urlReviews = Blueprint('views', __name__)

apiProj = API_CRUD_PROJECTS()
apiReviews = API_CRUD_REVIEWS(apiProj)


@urlReviews.route('/projects/<string:projectID>/addReview/<string:reviewID>', methods=['POST'])
def postReview(projectID, reviewID):
    reviewJson = request.json

    # get the project's review ids
    projectJson = apiProj.getProject(projectID)
    projectReviewsJson = projectJson['projectReviews']
    projectReviewsList = projectReviewsJson['reviews']

    # search for every userID in project's reviews
    for review_id in projectReviewsList:
        review = apiReviews.getReview(review_id)
        if review['userID'] == reviewJson['userID']:
            return { "ErrorMessage": "User already reviewed this project!"}

    reviewObj = Review(reviewID, reviewJson['userID'], projectID, reviewJson['review_description'], reviewJson['review_rating'])
    userID = reviewJson['userID']
    updateActivity(userID, "add_review", 2)
    return apiReviews.addReview(reviewObj)


@urlReviews.route('/reviews/<string:reviewID>', methods=['GET'])
def getReview(reviewID):
    return apiReviews.getReview(reviewID)


@urlReviews.route('/reviews/update/<string:projectID>/<string:reviewID>', methods=['PUT'])
def updateReview(projectID, reviewID):
    reviewJson = request.json
    return apiReviews.updateReview(reviewJson)

@urlReviews.route('/reviews/delete/<string:projectID>/<string:reviewID>', methods=['DELETE'])
def deleteReview(projectID, reviewID):
    return apiReviews.deleteReview(reviewID)
