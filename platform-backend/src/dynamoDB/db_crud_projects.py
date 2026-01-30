from boto3.dynamodb.conditions import Attr


class DB_CRUD_PROJECTS:
  def __init__(self, projectTable):
    """Initialize DB_CRUD_PROJECTS class

    Args:
        projectTable (_type_): db reference to the project table
    """
    self.__projectTable = projectTable

  def __exists(self, idOfTheProject: str):
    """Check if the project exists in the database

    Args:
        idOfTheProject (str): id of the project to check

    Returns:
        bool: True => project exists, False => project does not exist
    """
    response = self.__projectTable.get_item(
      Key={
        'id': idOfTheProject
      }
    )
    try:
      testVar = response["Item"]
      return True
    except KeyError:
      return False

  def fullscanProject(self):
    """Scan the entire project table

    Returns:
        list: list of all projects in the table
    """
    response = self.__projectTable.scan()
    data = response['Items']

    while 'LastEvaluatedKey' in response:
      response = self.__projectTable.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
      data.extend(response['Items'])
    return data

  def getProject(self, idOfTheProject: str):
    """Get a project from the database

    Args:
        idOfTheProject (str): id of the project to get

    Returns:
        dict: dictionary of the project
    """
    response = self.__projectTable.get_item(
      Key={
        'id': idOfTheProject
      }
    )
    try:
      return response["Item"]
    except KeyError:
      return {"ErrorMessage": "Project Does not Exist"}

  def getAllWithField(self, field: str):
    """Get all projects with a certain field (are of implementation)

    Args:
        field (str): Field to search for

    Returns:
        list: list of all projects with the field
    """
    response = self.__projectTable.scan(FilterExpression=Attr('areaOfImplementation').eq(field))
    return response['Items']

  def getAllFromOwner(self, owner_id: str):
    """Returns all projects from a certain owner

    Args:
        owner_id (str): id of the owner

    Returns:
        list: list of all projects owned by the user
    """
    listToReturn = []
    listOfProjects = self.__projectTable.scan()

    for project in listOfProjects['Items']:
      if owner_id in project['adminList']:
        listToReturn.append(project)
    return listToReturn

  def searchForProjectsThatStartWith(self, prefix: str):
    """Search for projects that start with a certain prefix

    Args:
        prefix (str): prefix to search for

    Returns:
        list: list of all projects that start with the prefix
    """
    response = self.__projectTable.scan(FilterExpression=Attr('searchTerm').contains(prefix.lower()))
    return response['Items']

  def addProject(self, projectObjJSON: dict):
    """Add project to the database

    Args:
        projectObjJSON (dict): dictionary of the project to add

    Returns:
        _type_: response
    """
    if not self.__exists(projectObjJSON['id']):
      response = self.__projectTable.put_item(
        Item=projectObjJSON
      )
    else:
      response = {
        "ErrorMessage": "Project already exists"
      }
    return response

  def updateProject(self, projectObjJSON):
    """Update a project in the database

    Args:
        projectObjJSON (dict): dictionary of the project to update

    Returns:
        _type_: response
    """
    if not self.__exists(projectObjJSON["id"]):
      return {"ErrorMessage": "Project Does not Exist"}

    response = self.__projectTable.update_item(
      Key={
        'id': projectObjJSON["id"]
      },
      UpdateExpression="set #nm=:n, #dscp=:d, #crtby=:c, #adml=:ad, #thm=:t, #thme=:te, #are=:a, #gls=:g, #mts=:m, #stgs=:st, #srch=:sterm, #rvs=:re, #mntfb=:mfb", 
      ExpressionAttributeValues={
        ':n': projectObjJSON["name"],
        ':d': projectObjJSON["description"],
        ':c': projectObjJSON['createdBy'],
        ':ad': projectObjJSON['adminList'],
        ':t': projectObjJSON["thumbnail"],
        ':te': projectObjJSON["thumbnail_extension"],
        ':a': projectObjJSON["areaOfImplementation"],
        ':g': projectObjJSON["goals"],
        ':m': projectObjJSON["materials"],
        ':st': projectObjJSON["settings"],
        ':sterm': projectObjJSON["searchTerm"],
        ':re': projectObjJSON["projectReviews"],
        ':mfb': projectObjJSON["mentor_feedback"],
      },
      ExpressionAttributeNames={
        "#nm": "name",
        "#dscp":"description",
        "#crtby": "createdBy",
        "#adml": "adminList",
        "#thm" : "thumbnail",
        "#thme": "thumbnail_extension",
        "#are":"areaOfImplementation",
        "#gls":"goals",
        "#mts": "materials",
        "#stgs":"settings",
        "#srch":"searchTerm",
        "#mntfb": "mentor_feedback",
        "#rvs":"projectReviews"
      },
      ReturnValues="UPDATED_NEW"
    )
    return response

  def deleteProject(self, idOfTheProject: str):
    """Delete a project from the database

    Args:
        idOfTheProject (str): id of the project to delete

    Returns:
        _type_: response
    """
    response = self.__projectTable.delete_item(
      Key={
        'id': idOfTheProject
      }
    )
    return response
