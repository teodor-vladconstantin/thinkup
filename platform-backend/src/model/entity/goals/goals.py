from model.entity.goals.goal import Goal

class Goals:
  def __init__(self, goals: list):
    self.__goals = goals

  def add_goal(self, goal: Goal):
    self.__goals.append(goal)

  def delete_goal(self, id: str):
    for goal in self.__goals:
      if goal.get_id() == id:
          self.__goals.remove(goal)

  def get_goals(self):
    return self.__goals