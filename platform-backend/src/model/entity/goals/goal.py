from model.entity.goals.objective import Objective


class Goal(Objective):
  def __init__(self, id: str, name: str, description: str, statePercentage: int, deadline: str, projectId: str):
    super().__init__(id, name, description, statePercentage, deadline)
    self.__projectId = projectId

  
  def get_projectId(self):
    return self.__projectId