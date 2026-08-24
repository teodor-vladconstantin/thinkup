from ..goals.goal import Goal

class GoalEncoder():
  def toJson(goal):
    if isinstance(goal, Goal):
      newItem = {
        'id': goal.get_id(),
        'name': goal.get_name(),
        'description': goal.get_description(),
        'state': goal.get_statePercentage(),
        'deadline': goal.get_deadline(),
        'projectId': goal.get_projectId(),
      }
      return newItem
    return None

"""
JSON Format:

{
    "name": "nume objectiv",
    "description": "obiectiv de test",
    "state": 15,
    "deadline": "11/2/2023",
    "projectId": "118123136512061879318"
}
"""