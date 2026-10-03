import os

import flask
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from utils.logger import setup_logger
from model.entity.open_school.open_school import OPEN_SCHOOL
from views.view_challenges import urlChallenges
from views.view_files import urlFiles
from views.view_gmail_contact import urlContact
from views.view_goals import urlGoals
from views.view_materials import urlMaterial
from views.view_mentor_feedback import urlFeedback
from views.view_openSchool import urlOpenSchool
from views.view_personal_objectives import urlPersonalObjectives
from views.view_projects import urlProject
from views.view_reviews import urlReviews
from views.view_submissions import urlSubmissions
from views.view_thumbnails import urlThumbnails
from views.view_users import urlUser
from views.view_warnings import urlWarnings

logger = setup_logger(__name__)
logger.info("Reloading Backend...")
app = flask.Flask(__name__)
# In production nginx serves frontend and API on one origin; CORS only matters for local dev
CORS(app, origins=os.environ.get("CORS_ORIGINS", "http://localhost:3000").split(","))


# abort(...) returns JSON so the frontend can read err.response.data.error
@app.errorhandler(HTTPException)
def handle_http_exception(e):
    return flask.jsonify({"error": e.description}), e.code


@app.errorhandler(KeyError)
def handle_missing_field(e):
    return flask.jsonify({"error": f"Missing field: {e}"}), 400


@app.errorhandler(Exception)
def handle_unexpected(e):
    # Log the details, never send them to the client
    logger.error(f"Unhandled error on {flask.request.method} {flask.request.path}", exc_info=e)
    return flask.jsonify({"error": "Internal server error"}), 500


openSchool = OPEN_SCHOOL('thinkup-open-school')

app.register_blueprint(urlUser)
app.register_blueprint(urlProject, name='Proj')
app.register_blueprint(urlFiles, name='Fils')
app.register_blueprint(urlMaterial, name='Mats')
app.register_blueprint(urlThumbnails, name='Thumb')
app.register_blueprint(urlGoals, name='Gls')
app.register_blueprint(urlContact, name='Contact')
app.register_blueprint(urlOpenSchool, name='School')
app.register_blueprint(urlPersonalObjectives, name='PersObj')
app.register_blueprint(urlReviews, name='Rev')
app.register_blueprint(urlFeedback, name="Feedb")
app.register_blueprint(urlChallenges, name="Chall")
app.register_blueprint(urlSubmissions, name="Subm")
app.register_blueprint(urlWarnings, name="Warn")


if __name__ == "__main__":
    app.run(debug=True)
