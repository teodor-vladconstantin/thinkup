from model.entity.mentor_feedback.mentor_feedback import MENTOR_FEEDBACK


class MentorFeedbackEncoder:
  def toJSON(o):
    if isinstance(o, MENTOR_FEEDBACK):
        Item = {
          'id': o.get_id(),
          'mentor_id': o.get_mentor_id(),
          'feedback_txt': o.get_feedback_txt(),
          'date': o.get_date(),
          'project_id': o.get_project_id(),
        }
        return Item
    return None
