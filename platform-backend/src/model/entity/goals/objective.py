class Objective:
  def __init__(self, id: str, name: str, description: str, statePercentage: int, deadline: str):
    self.__id = id
    self.__name = name
    self.__description = description
    self.__statePercentage = statePercentage
    self.__deadline = deadline

  def get_id(self):
    return self.__id

  def get_name(self):
    return self.__name
    
  def set_name(self, name: str):
    self.__name = name

  def get_description(self):
    return self.__description

  def set_description(self, description: str):
    self.__description = description

  def get_statePercentage(self):
    return self.__statePercentage

  def set_statePercentage(self, newStatePercentage: int):
    self.__statePercentage = newStatePercentage

  def get_deadline(self):
    return self.__deadline

  def set_deadline(self, deadline: str):
    self.__deadline = deadline
    