from api.api_crud_personal_objectives import API_CRUD_PERSONAL_OBJECTIVES
from flask import Blueprint, request
from model.entity.goals.personal_objective import PersonalObjective

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
def postObjective(id: str):
  """Post a personal objective to database

  Args:
      id (str): id of the personal objective

  Returns:
      _type_: response
  """
  objectiveJson = request.json
  objectiveObj = PersonalObjective(id, objectiveJson['name'], objectiveJson['description'], objectiveJson['statePercentage'], objectiveJson['deadline'], objectiveJson['userId'])

  return apiPesonalObjectives.addPersonalObjective(objectiveObj)

@urlPersonalObjectives.route('/personal_objectives/<string:id>', methods=['DELETE'])
def deleteObjective(id: str):
  """Delete a personal objective from database

  Args:
      id (str): id of the personal objective

  Returns:
      _type_: response
  """
  return apiPesonalObjectives.deletePersonalObjective(id)

@urlPersonalObjectives.route('/personal_objectives/<string:id>', methods=['PUT'])
def updateObjective(id: str):
  """Update a personal objective from database

  Args:
      id (str): id of the personal objective
  """
  personalObjJson = request.json 
  apiPesonalObjectives.updatePersonalObjective(id, personalObjJson)
