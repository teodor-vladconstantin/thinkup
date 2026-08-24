from ctypes import c_longlong as ll

class File:
  def __init__(self, fileId, fileSize: ll, fileName: str, fileExtension: str, fileType: str, materialId: str):
    self.__fileId = fileId
    self.__fileSize = fileSize
    self.__fileExtension = fileExtension
    self.__fileType = fileType
    self.__fileName = fileName
    self.__materialId = materialId

  def get_fileName(self):
    return self.__fileName

  def get_fileId(self):
    return self.__fileId
  
  def get_fileSize(self):
    return self.__fileSize

  def get_fileExtension(self):
    return self.__fileExtension

  def get_fileType(self):
    return self.__fileType

  def get_materialId(self):
    return self.__materialId