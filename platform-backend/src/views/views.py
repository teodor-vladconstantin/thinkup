import flask
from flask import Blueprint


urlBP = Blueprint('views', __name__)

@urlBP.route('/')
def test_page():
  return flask.render_template("test_page.html")

# perms = {
#     'canCreateProject': True,
#     'canEditProject': True, 
#     'canDeleteProject': False
# }

# settings = Settings("ro", True, False)
# permissions = Permissions(perms)

# dbCrudUsers = setup.startSetup('Users') # Gets the dbCrudUsers Obj
# dbCrudProjects = setup.startSetup('Projects')
# dbCurdGoals = setup.startSetup('Goals')
# s3Crud = S3_OPERATIONS('thinkup-logos')

# apiUsers = API_CRUD_USERS(dbCrudUsers)
# apiProjects = API_CRUD_PROJECTS(dbCrudProjects)