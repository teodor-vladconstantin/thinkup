import os

import flask
from flask_cors import CORS

from utils.logger import setup_logger
from model.entity.open_school.open_school import OPEN_SCHOOL
from views.view_files import urlFiles
from views.view_gmail_contact import urlContact
from views.view_goals import urlGoals
from views.view_materials import urlMaterial
from views.view_mentor_feedback import urlFeedback
from views.view_openSchool import urlOpenSchool
from views.view_personal_objectives import urlPersonalObjectives
from views.view_projects import urlProject
from views.view_reviews import urlReviews
from views.view_thumbnails import urlThumbnails
from views.view_users import urlUser
from views.views import urlBP

logger = setup_logger(__name__)
logger.info("Reloading Backend...")
app = flask.Flask(__name__)

allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000,https://thinkupacademy.ro",
    ).split(",")
    if origin.strip()
]

CORS(
    app,
    resources={r"/*": {"origins": allowed_origins}},
    supports_credentials=True,
)


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
app.register_blueprint(urlBP, name='testURL')
app.register_blueprint(urlFeedback, name="Feedb")


if __name__ == "__main__":
    app.run(debug=True)
