from api.api_crud_goals import API_CRUD_GOALS
from dynamoDB import setup
from flask import Blueprint, request
from model.entity.goals.goal import Goal
from utils.jwt_server import require_auth

urlGoals = Blueprint('views', __name__)

dbCrudGoals = setup.startSetup('Goals')
apiGoals = API_CRUD_GOALS(dbCrudGoals)

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
  return apiGoals.deleteGoal(id)

@urlGoals.route('/goals/<string:id>', methods=['PUT'])
@require_auth()
def updateGoal(id: str):
  """Update a goal in the database

  Args:
      id (str): id of the goal to be updated
  """
  goalJson = request.json
  apiGoals.updateGoal(goalJson)
