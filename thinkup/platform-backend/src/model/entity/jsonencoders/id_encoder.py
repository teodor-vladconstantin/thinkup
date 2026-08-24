
from model.entity.file.file import File


class IdEncoder():
  def toJson(file):
    if isinstance(file, File):
      newItem = {
        'id': file.get_fileId(),
        'name': file.get_fileName(),
        'extension': file.get_fileExtension(),
        'file_type': file.get_fileType(),
        'materialId': file.get_materialId(),
      }
      return newItem
    return None