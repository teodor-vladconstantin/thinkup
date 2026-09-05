from api.api_crud_mentor_feedback import API_CRUD_MENTOR_FEEDBACK
from dynamoDB import setup
from flask import Blueprint, request, abort
from model.entity.mentor_feedback.mentor_feedback import MENTOR_FEEDBACK
from datetime import datetime
from utils.jwt_server import require_auth, current_user_id

urlFeedback = Blueprint("views", __name__)

apiFeedback = API_CRUD_MENTOR_FEEDBACK()
dbCrudUsers = setup.startSetup('Users')

@urlFeedback.route('/projects/<string:pid>/feedback/<string:fid>', methods=["POST"])
@require_auth()
def addFeedback(pid: str, fid: str):
  """Add feedback to project

  Args:
      pid (str): id of the project
      fid (str): id of the feedback

  Returns:
      _type_: response
  """
  mentor_id = current_user_id()
  mentor = dbCrudUsers.getUser(mentor_id)
  if not mentor or "ErrorMessage" in mentor:
      abort(403, description="You are not authorized to add feedback")
  if mentor.get('role') != 'Mentor':
      abort(403, description="Only mentors can add feedback")

  feedback_json = request.json
  feedback_obj = MENTOR_FEEDBACK(fid, mentor_id, feedback_json["feedback_txt"],  datetime.now().strftime("%d/%m/%Y %H:%M:%S"), pid)


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
@require_auth()
def deleteFeedback(pid: str, fid: str):
  """Delete a feedback

  Args:
      uid (str): id of the project
      fid (str): id of the feedback to delete

  Returns:
      _type_: response
  """
  existing = apiFeedback.getFeedback(fid)
  if not existing or 'mentor_id' not in existing:
      abort(404, description="Feedback does not exist")
  if existing['mentor_id'] != current_user_id():
      abort(403, description="You can only delete your own feedback")

  return apiFeedback.deleteFeedback(fid, pid)


@urlFeedback.route('/projects/<string:pid>/feedback/<string:fid>', methods=["PUT"])
@require_auth()
def editFeedack(pid: str, fid: str):
  """Edit feedback:
  Args:
    pid (str): id of the project
    fid (str): id of the feedback to update/edit
  Returns:
    _type_: response
  """
  existing = apiFeedback.getFeedback(fid)
  if not existing or 'mentor_id' not in existing:
      abort(404, description="Feedback does not exist")
  if existing['mentor_id'] != current_user_id():
      abort(403, description="You can only edit your own feedback")

  updated_feedback = request.json
  updated_feedback_obj = MENTOR_FEEDBACK(fid, current_user_id(), updated_feedback["feedback_txt"], datetime.now().strftime("%d/%m/%Y %H:%M:%S"),pid)
  return apiFeedback.editFeedback(fid,pid, updated_feedback_obj)


