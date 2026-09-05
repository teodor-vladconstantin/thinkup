from api.api_crud_projects import API_CRUD_PROJECTS
from api.api_crud_reviews import API_CRUD_REVIEWS
from api.api_track_activity import updateActivity
from dynamoDB import setup
from flask import Blueprint, request, abort
from model.entity.reviews.review import Review
from utils.jwt_server import require_auth, current_user_id

urlReviews = Blueprint('views', __name__)

apiProj = API_CRUD_PROJECTS()
apiReviews = API_CRUD_REVIEWS(apiProj)


@urlReviews.route('/projects/<string:projectID>/addReview/<string:reviewID>', methods=['POST'])
@require_auth()
def postReview(projectID, reviewID):
    reviewJson = request.json
    user_id = current_user_id()

    # get the project's review ids
    projectJson = apiProj.getProject(projectID)
    projectReviewsJson = projectJson['projectReviews']
    projectReviewsList = projectReviewsJson['reviews']

    # search for every userID in project's reviews
    for review_id in projectReviewsList:
        review = apiReviews.getReview(review_id)
        if review['userID'] == user_id:
            return { "ErrorMessage": "User already reviewed this project!"}

    reviewObj = Review(reviewID, user_id, projectID, reviewJson['review_description'], reviewJson['review_rating'])
    updateActivity(user_id, "add_review", 2)
    return apiReviews.addReview(reviewObj)


@urlReviews.route('/reviews/<string:reviewID>', methods=['GET'])
def getReview(reviewID):
    return apiReviews.getReview(reviewID)


@urlReviews.route('/reviews/update/<string:projectID>/<string:reviewID>', methods=['PUT'])
@require_auth()
def updateReview(projectID, reviewID):
    existing = apiReviews.getReview(reviewID)
    if not existing or 'userID' not in existing:
        abort(404, description="Review does not exist")
    if existing['userID'] != current_user_id():
        abort(403, description="You can only edit your own review")

    reviewJson = request.json
    reviewJson['id'] = reviewID
    reviewJson['userID'] = current_user_id()
    return apiReviews.updateReview(reviewJson)

@urlReviews.route('/reviews/delete/<string:projectID>/<string:reviewID>', methods=['DELETE'])
@require_auth()
def deleteReview(projectID, reviewID):
    existing = apiReviews.getReview(reviewID)
    if not existing or 'userID' not in existing:
        abort(404, description="Review does not exist")
    if existing['userID'] != current_user_id():
        abort(403, description="You can only delete your own review")

    return apiReviews.deleteReview(reviewID)
