from ..challenge import Challenge


class ChallengeEncoder():
  def toJSON(o):
    if isinstance(o, Challenge):
      Item = {
        'id': o.get_id(),
        'name': o.get_name(),
        'description': o.get_description(),
        'deadline': o.get_deadline(),
        'maxScore': o.get_maxScore(),
        'createdBy': o.get_createdBy(),
        'creationDate': o.get_creationDate(),
      }
      return Item
    return None


# USE : ChallengeEncoder().toJSON(challenge)

"""
JSON Format :

{
    "id": "challenge1",
    "name": "Build a recycling tracker",
    "description": "Prototype an app that tracks recycling habits",
    "deadline": "2026-10-01T00:00:00",
    "maxScore": 100,
    "createdBy": "mentorUserId",
    "creationDate": "2026-09-04"
}
"""
