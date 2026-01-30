from dynamoDB import setup
from model.entity.jsonencoders.mentor_feedback_encoder import \
    MentorFeedbackEncoder
from model.entity.mentor_feedback.mentor_feedback import MENTOR_FEEDBACK

from api.api_crud_projects import API_CRUD_PROJECTS


class API_CRUD_MENTOR_FEEDBACK:
  def __init__(self):
    """Initialize the class """
    self.__db_crud_feedback = setup.startSetup('Mentor-Feedback')
    self.__apiProj = API_CRUD_PROJECTS()
  
  def getFeedback(self, idOfTheFeedback: str):
    """Get a feedback from database

    Args:
        idOfTheFeedback (str): id of the feedback

    Returns:
        dict: dictionary with the feedback
    """
    return self.__db_crud_feedback.getFeedback(idOfTheFeedback)

  def addFeedback(self, mentor_feedback: MENTOR_FEEDBACK, projectId: str):
    """Add mentor feedback to a proejct

    Args:
        mentor_feedback (MENTOR_FEEDBACK): feedback to add
        projectId (str): id of the project to add the feedback to

    Returns:
        _type_: response
    """
    # Add to project
    projJson = self.__apiProj.getProject(projectId)
    projJson2 = projJson

    projJson['mentor_feedback'].insert(0, mentor_feedback.get_id())
    self.__apiProj.updateProject(projJson2, projJson, None)

    return self.__db_crud_feedback.addFeedback(MentorFeedbackEncoder.toJSON(mentor_feedback))

  def deleteFeedback(self, idOfFeedback: str, idOfProj: str):
    """Delete a feedback from project

    Args:
        idOfFeedback (str): id of the feedback
        idOfProj (str): id of the project

    Returns:
        _type_: response
    """
    projJson = self.__apiProj.getProject(idOfProj)
    projJson2 = projJson
    projJson['mentor_feedback'].remove(idOfFeedback)

    self.__apiProj.updateProject(projJson2, projJson, None)

    return self.__db_crud_feedback.deleteFeedback(idOfFeedback)

  
  def editFeedback(self, idOfFeedback: str, idOfProj: str, updatedFeedback: MENTOR_FEEDBACK):
      """
      Edits a feedback from the database
      """
      projJson = self.__apiProj.getProject(idOfProj)
      projJson2 = projJson

      updatedFeedbackJSON = MentorFeedbackEncoder.toJSON(updatedFeedback)

      projJson['mentor_feedback'].remove(idOfFeedback)
      projJson['mentor_feedback'].insert(0, updatedFeedbackJSON['id'])
      self.__apiProj.updateProject(projJson2, projJson, None)

      return self.__db_crud_feedback.editFeedback(idOfFeedback, updatedFeedbackJSON)
