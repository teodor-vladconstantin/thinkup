from dynamoDB import setup
from model.entity.goals.personal_objective import PersonalObjective
from model.entity.jsonencoders.personal_objective_encoder import \
    PersonalObjectiveEncoder
from s3.s3_crud import S3_OPERATIONS

from api.api_crud_users import API_CRUD_USERS


class API_CRUD_PERSONAL_OBJECTIVES:
  def __init__(self):
    """Initialize the class"""
    self.__db_crud_personal_objectives = setup.startSetup('Personal-Objectives')
    self.__apiUsers = API_CRUD_USERS()

  def getPersonalObjective(self, idOfTheObjective: str):
    """Get a personal objective from database

    Args:
        idOfTheObjective (str): id of the personal objective

    Returns:
        dict: dictionary with the personal objective
    """
    return self.__db_crud_personal_objectives.getObjective(idOfTheObjective)
  
  def addPersonalObjective(self, personal_objective: PersonalObjective):
    """Add a personal objective to database

    Args:
        personal_objective (PersonalObjective): personal objective to add

    Returns:
        _type_: response
    """
    # Add to user
    userJson = self.__apiUsers.getUser(personal_objective.get_userId())
    userJson2 = userJson

    userJson['personal_objectives'].insert(0, personal_objective.get_id())
    self.__apiUsers.updateUser(userJson2, userJson, None)

    return self.__db_crud_personal_objectives.addObjective(PersonalObjectiveEncoder.toJson(personal_objective))

  def updatePersonalObjective(self, id: str, personal_objectiveJson: dict):
    """Update a personal objective in the database

    Args:
        id (str): id of the personal objective
        personal_objectiveJson (dict): dictionary of personal objective

    Returns:
        _type_: response
    """
    poJson = self.__db_crud_personal_objectives.getObjective(id)

    try:
      poJson['name'] = personal_objectiveJson['name']
    except KeyError:
      pass

    try:
      poJson['description'] = personal_objectiveJson['description']
    except KeyError:
      pass

    try:
      poJson['statePercentage'] = personal_objectiveJson['statePercentage']
    except KeyError:
      pass

    try:
      poJson['deadline'] = personal_objectiveJson['deadline']
    except KeyError:
      pass

    return self.__db_crud_personal_objectives.updateObjective(poJson)

  def deletePersonalObjective(self, idOfPersonalObjective: str):
    """Delete a personal objective from database

    Args:
        idOfPersonalObjective (str): id of the personal objective

    Returns:
        _type_: response
    """
    personal_objectiveJson = self.getPersonalObjective(idOfPersonalObjective)
    userJson = self.__apiUsers.getUser(personal_objectiveJson['userId'])
    userJson2 = userJson
    userJson['personal_objectives'].remove(idOfPersonalObjective)

    self.__apiUsers.updateUser(userJson2, userJson, None, None)

    return self.__db_crud_personal_objectives.deleteObjective(idOfPersonalObjective)
