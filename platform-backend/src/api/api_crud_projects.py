import operator
import os

from dynamoDB import setup
from model.entity.jsonencoders.project_encoder import ProjectEncoder
from model.entity.project import Project
from s3.s3_crud import S3_OPERATIONS
from api.api_track_activity import updateActivity


class API_CRUD_PROJECTS:
  def __init__(self) :
    """Initialize the API_CRUD_PROJECTS class
    """
    self.__dbCrudProjects = setup.startSetup('Projects')
    self.__s3Thumbnail = S3_OPERATIONS('thinkup-thumbnail')
    self.__dbCrudTokens = setup.startSetup('Project-Tokens')

  def __deleteProjectToken (self, projectToken: str):
    """Delete a project token from the database

    Args:
        projectToken (str): the project token

    Returns:
        _type_: response
    """
    return self.__dbCrudTokens.deleteToken(projectToken)

  def isTokenValid (self, token: str):
    """Check if a token is valid

    Args:
        token (str): token to check

    Returns:
        bool: True => the token is valid, False => otherwise
    """
    return self.__dbCrudTokens.isTokenValid(token)
  
  def getProject (self, idOfTheProject: str):
    """Get a project by id

    Args:
        idOfTheProject (str): id of the project

    Returns:
        dict: dictionary with the project
    """
    return self.__dbCrudProjects.getProject(idOfTheProject)

  def getAllProjects (self, filter: str):
    """Returns all existing projects with / without a specific are of implementation

    Args:
        filter (str): filter to apply to the projects (optional)

    Returns:
        list: list of all projects
    """
    if filter is None:
      data = self.__dbCrudProjects.fullscanProject()
      Item = {
        'projects': data
      }
      Item['projects'].sort(key=operator.itemgetter('name'))
      return Item
    else:
      data = self.__dbCrudProjects.getAllWithField(filter)
      Item = {
        'projects': data
      }
      Item['projects'].sort(key=operator.itemgetter('name'))
      return Item

  def getOwnedProjects(self, owner_id: str):
    """Get projects owned by a specific user

    Args:
        owner_id (str): id of the user

    Returns:
        list: list of projects owned by the user
    """
    if owner_id is None:
      data = self.__dbCrudProjects.fullscanProject
      Item = {
        'projects': data
      }
      Item['projects'].sort(key=operator.itemgetter('name'))
      return Item
    else:
      data = self.__dbCrudProjects.getAllFromOwner(owner_id)
      Item = {
          'projects': data
      }
      Item['projects'].sort(key=operator.itemgetter('name'))
      return Item

  def searchProject(self, prefix: str):
    """Search for a project by name

    Args:
        prefix (str): prefix to search for

    Returns:
        dict: dictionary with the project
    """
    data = self.__dbCrudProjects.searchForProjectsThatStartWith(prefix)
    Item = {
      'projects': data
    }
    return Item

  def addProject (self, project_token: str, project_object: Project):
    """Add a new project to the database
    Args:
        project_token (str): authorization token for creating a project
        project_object (Project): project to add
    Returns:
        _type_: response
    """
    self.__deleteProjectToken(project_token)
    return self.__dbCrudProjects.addProject(ProjectEncoder.toJSON(project_object))

  def updateProject (self, projectToUpdate: dict, projectJson: dict, thumbnail):
    """Update a project

    Args:
        projectToUpdate (dict): initial project attributes
        projectJson (dict): updated project attributes
        thumbnail (_type_): new project thumbnail; null

    Returns:
        _type_: _description_
    """
    deletePreviousPicture = False;
    previousPictureId = None
    

    try:
      projectToUpdate['materials'] = projectJson['materials']
    except KeyError:
      pass

    try:
      projectToUpdate['name'] = projectJson['name']
    except KeyError:
      pass

    try:
      projectToUpdate['searchTerm'] = str(projectJson['name']).lower()
    except KeyError:
      pass

    try:
      projectToUpdate['goals'] = projectJson['goals']
    except KeyError:
      pass

    try:
      projectToUpdate['description'] = projectJson['description']
    except KeyError:
      pass
    
    try:
      projectToUpdate['areaOfImplementation'] = projectJson['areaOfImplementation']
    except KeyError:
      pass

    try:
      projectToUpdate['projectReviews'] = projectJson['projectReviews']
    except KeyError:
      pass

    try:
      print(f"{projectToUpdate['adminList']} and {projectJson['adminList']}")
      projectToUpdate["adminList"].extend(projectJson["adminList"])
      projectToUpdate["adminList"] = list(set(projectToUpdate["adminList"]))
    except KeyError:
      pass

    
    if projectToUpdate["thumbnail"][0:7] != "default" and thumbnail is not None:
      deletePreviousPicture = True
      previousPictureId = projectToUpdate["thumbnail"]
      projectToUpdate['thumbnail'] = projectJson['thumbnail']

    if thumbnail is not None:
      projectToUpdate['thumbnail'] = projectJson['thumbnail']
      pathname, extension = os.path.splitext(thumbnail.filename)
      new_name = projectToUpdate["thumbnail"] + extension
      
      self.__s3Thumbnail.Upload(new_name, thumbnail, False)
      # Delete past profile pic
      if deletePreviousPicture is True:
        self.__s3Thumbnail.Delete(previousPictureId, projectToUpdate["thumbnail_extension"])
      projectToUpdate["thumbnail_extension"] = extension

    return self.__dbCrudProjects.updateProject(projectToUpdate)

  def deleteProject (self, idOfTheProject: str):
    """Delete a project from the database

    Args:
        idOfTheProject (str): id of the project

    Returns:
        _type_: response
    """
    return self.__dbCrudProjects.deleteProject(idOfTheProject)
