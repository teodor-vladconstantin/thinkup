from ..goals.personal_objective import PersonalObjective

class PersonalObjectiveEncoder():
  def toJson(goal):
    if isinstance(goal, PersonalObjective):
      newItem = {
        'id': goal.get_id(),
        'name': goal.get_name(),
        'description': goal.get_description(),
        'state': goal.get_statePercentage(),
        'deadline': goal.get_deadline(),
        'userId': goal.get_userId(),
      }
      return newItem
    return None

"""
JSON Format :

  {
    "name": "nume objectiv",
    "description": "obiectiv de test",
    "statePercentage": 15,
    "deadline": "11/2/2023",
    "userId": "118123136512061879318"
  }
"""