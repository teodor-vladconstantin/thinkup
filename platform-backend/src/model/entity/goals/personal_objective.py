from model.entity.goals.objective import Objective

class PersonalObjective(Objective):
  def __init__(self, id: str, name: str, description: str, statePercentage: int, deadline: str, user_id: str):
    super().__init__(id, name, description, statePercentage, deadline)
    self.__user_id = user_id

  def get_userId(self):
    return self.__user_id