class MENTOR_FEEDBACK:
  def __init__(self, id: str, mentor_id: str, feedback_txt: str, date: str, project_id: str):
    self.__id = id
    self.__mentor_id = mentor_id
    self.__feedback_txt = feedback_txt
    self.__date = date
    self.__project_id = project_id

  def get_id(self):
    return self.__id

  def get_mentor_id(self):
    return self.__mentor_id

  def get_feedback_txt(self):
    return self.__feedback_txt

  def get_date(self):
    return self.__date
  
  def get_project_id(self):
    return self.__project_id
