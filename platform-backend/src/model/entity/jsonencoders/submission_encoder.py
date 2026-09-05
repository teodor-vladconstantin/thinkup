from ..submission import Submission


class SubmissionEncoder():
  def toJSON(o):
    if isinstance(o, Submission):
      Item = {
        'id': o.get_id(),
        'studentId': o.get_studentId(),
        'challengeId': o.get_challengeId(),
        'score': o.get_score(),
        'gradedBy': o.get_gradedBy(),
        'gradedDate': o.get_gradedDate(),
        'feedback': o.get_feedback(),
        'projectId': o.get_projectId(),
      }
      return Item
    return None


# USE : SubmissionEncoder().toJSON(submission)

"""
JSON Format :

{
    "id": "submission1",
    "studentId": "studentUserId",
    "challengeId": "challenge1",
    "score": 85,
    "gradedBy": "mentorUserId",
    "gradedDate": "2026-09-04T12:00:00",
    "feedback": "Great work, could improve the UI"
}
"""
