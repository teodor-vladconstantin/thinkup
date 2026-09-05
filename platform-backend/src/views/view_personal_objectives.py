from api.api_crud_personal_objectives import API_CRUD_PERSONAL_OBJECTIVES
from flask import Blueprint, request, abort
from model.entity.goals.personal_objective import PersonalObjective
from utils.jwt_server import require_auth, current_user_id

urlPersonalObjectives = Blueprint('views', __name__)

apiPesonalObjectives = API_CRUD_PERSONAL_OBJECTIVES()

@urlPersonalObjectives.route('/personal_objectives/<string:id>', methods=['GET'])
def getObjective(id: str):
  """Get a personal objective from database

  Args:
      id (str): id of the personal objective

  Returns:
      dict: dictionary with the personal objective
  """
  return apiPesonalObjectives.getPersonalObjective(id)

@urlPersonalObjectives.route('/personal_objectives/<string:id>', methods=['POST'])
@require_auth()
def postObjective(id: str):
  """Post a personal objective to database

  Args:
      id (str): id of the personal objective

  Returns:
      _type_: response
  """
  objectiveJson = request.json
  objectiveObj = PersonalObjective(id, objectiveJson['name'], objectiveJson['description'], objectiveJson['statePercentage'], objectiveJson['deadline'], current_user_id())

  return apiPesonalObjectives.addPersonalObjective(objectiveObj)

@urlPersonalObjectives.route('/personal_objectives/<string:id>', methods=['DELETE'])
@require_auth()
def deleteObjective(id: str):
  """Delete a personal objective from database

  Args:
      id (str): id of the personal objective

  Returns:
      _type_: response
  """
  existing = apiPesonalObjectives.getPersonalObjective(id)
  if not existing or 'userId' not in existing:
      abort(404, description="Objective does not exist")
  if existing['userId'] != current_user_id():
      abort(403, description="You can only delete your own objectives")

  return apiPesonalObjectives.deletePersonalObjective(id)

@urlPersonalObjectives.route('/personal_objectives/<string:id>', methods=['PUT'])
@require_auth()
def updateObjective(id: str):
  """Update a personal objective from database

  Args:
      id (str): id of the personal objective
  """
  existing = apiPesonalObjectives.getPersonalObjective(id)
  if not existing or 'userId' not in existing:
      abort(404, description="Objective does not exist")
  if existing['userId'] != current_user_id():
      abort(403, description="You can only edit your own objectives")

  personalObjJson = request.json
  return apiPesonalObjectives.updatePersonalObjective(id, personalObjJson)
