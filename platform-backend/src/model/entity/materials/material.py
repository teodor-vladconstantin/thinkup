class Material:
  def __init__(self, id: str, name: str, projectId: str, description: str, creationDate: str, createdBy: str, files: list):
    self.__id = id
    self.__name = name
    self.__projectId = projectId
    self.__description = description
    self.__creationDate = creationDate
    self.__createdBy = createdBy
    self.__files = files

  def get_id(self):
    return self.__id

  def get_name(self):
    return self.__name

  def set_name(self, new_name: str):
    self.__name = new_name

  def get_description(self):
    return self.__description

  def set_description(self, new_description: str):
    self.__description = new_description

  def get_creationDate(self):
    return self.__creationDate

  def add_file(self, new_file: str):
    self.__files.append(new_file)

  def delete_file(self, index_of_file: int):
    self.__files.pop(index_of_file)

  def get_files(self):
    return self.__files

  def get_createdBy(self):
    return self.__createdBy

  def get_projectId(self):
    return self.__projectId