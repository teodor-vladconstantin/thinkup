from api.api_crud_goals import API_CRUD_GOALS
from api.api_crud_projects import API_CRUD_PROJECTS
from dynamoDB import setup
from flask import Blueprint, request, abort
from model.entity.goals.goal import Goal
from utils.jwt_server import require_auth, current_user_id

urlGoals = Blueprint('views', __name__)

dbCrudGoals = setup.startSetup('Goals')
apiGoals = API_CRUD_GOALS(dbCrudGoals)
apiProjects = API_CRUD_PROJECTS()


def _is_project_owner(project, user_id):
  """Check if user_id is the creator or an admin of the given project dict.

  Note: user_id is a value the client supplies (see PUT /projects/<id> for
  why - the JWT is a service-to-service M2M token, not per-user).
  """
  if not project or "ErrorMessage" in project or not user_id:
    return False
  return project.get('createdBy') == user_id or user_id in project.get('adminList', [])


@urlGoals.route('/goals/<string:id>', methods=['GET'])
def getGoal(id: str):
  """Get a goal from the database

  Args:
      id (str): id of the goal

  Returns:
      JSON: the goal in JSON format
  """
  return apiGoals.getGoal(id)

@urlGoals.route('/goals/<string:id>', methods=['POST'])
@require_auth()
def postGoal(id: str):
  """Add a goal to the database

  Args:
      id (str): id of the goal

  Returns:
      _type_: response
  """
  goalJson = request.json
  if not goalJson:
    abort(400, description="Missing JSON body")

  project = apiProjects.getProject(goalJson.get('projectId'))
  if not _is_project_owner(project, current_user_id()):
    abort(403, description="You are not authorized to add goals to this project")

  goalObj = Goal(id, goalJson['name'], goalJson['description'], goalJson['statePercentage'], goalJson['deadline'], goalJson['projectId'])

  return apiGoals.addGoal(goalObj)

@urlGoals.route('/goals/<string:id>', methods=['DELETE'])
@require_auth()
def deleteGoal(id: str):
  """Delete a goal from the database

  Args:
      id (str): id of the goal to be deleted

  Returns:
      _type_: response
  """
  goal = apiGoals.getGoal(id)
  if not goal or "ErrorMessage" in goal:
    abort(404, description="Goal not found")

  project = apiProjects.getProject(goal.get('projectId'))
  if not _is_project_owner(project, current_user_id()):
    abort(403, description="You are not authorized to delete this goal")

  return apiGoals.deleteGoal(id)

@urlGoals.route('/goals/<string:id>', methods=['PUT'])
@require_auth()
def updateGoal(id: str):
  """Update a goal in the database

  Args:
      id (str): id of the goal to be updated
  """
  goalJson = request.json
  if not goalJson:
    abort(400, description="Missing JSON body")

  goal = apiGoals.getGoal(id)
  if not goal or "ErrorMessage" in goal:
    abort(404, description="Goal not found")

  project = apiProjects.getProject(goal.get('projectId'))
  if not _is_project_owner(project, current_user_id()):
    abort(403, description="You are not authorized to update this goal")

  return apiGoals.updateGoal(goalJson)
