from api.api_crud_mentor_feedback import API_CRUD_MENTOR_FEEDBACK
from flask import Blueprint, request
from model.entity.mentor_feedback.mentor_feedback import MENTOR_FEEDBACK
from datetime import datetime

urlFeedback = Blueprint("views", __name__)

apiFeedback = API_CRUD_MENTOR_FEEDBACK()

@urlFeedback.route('/projects/<string:pid>/feedback/<string:fid>', methods=["POST"])
def addFeedback(pid: str, fid: str):
  """Add feedback to project

  Args:
      pid (str): id of the project
      fid (str): id of the feedback

  Returns:
      _type_: response
  """
  feedback_json = request.json
  feedback_obj = MENTOR_FEEDBACK(fid, feedback_json["mentor_id"], feedback_json["feedback_txt"],  datetime.now().strftime("%d/%m/%Y %H:%M:%S"), pid)


  return apiFeedback.addFeedback(feedback_obj, pid)

@urlFeedback.route('/projects/<string:pid>/feedback/<string:fid>', methods=["GET"])
def getFeedback(pid: str, fid: str):
  """Get feedback

  Args:
      fid (str): id of the feedback to get

  Returns:
      dict: dict of specific feedback
  """
  print(fid)
  return apiFeedback.getFeedback(fid)

@urlFeedback.route('/projects/<string:pid>/feedback/<string:fid>', methods=["DELETE"])
def deleteFeedback(pid: str, fid: str):
  """Delete a feedback

  Args:
      uid (str): id of the project
      fid (str): id of the feedback to delete

  Returns:
      _type_: response
  """
  return apiFeedback.deleteFeedback(fid, pid)


@urlFeedback.route('/projects/<string:pid>/feedback/<string:fid>', methods=["PUT"])
def editFeedack(pid: str, fid: str):
  """Edit feedback:
  Args:
    pid (str): id of the project 
    fid (str): id of the feedback to update/edit
  Returns:
    _type_: response 
  """  
  updated_feedback = request.json
  updated_feedback_obj = MENTOR_FEEDBACK(fid, updated_feedback["mentor_id"], updated_feedback["feedback_txt"], datetime.now().strftime("%d/%m/%Y %H:%M:%S"),pid)
  return apiFeedback.editFeedback(fid,pid, updated_feedback_obj)


