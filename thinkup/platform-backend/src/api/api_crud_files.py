import os
import pathlib

from dynamoDB import setup
from flask import send_file
from model.entity.file.file import File
from model.entity.jsonencoders.id_encoder import IdEncoder
from s3.s3_crud import S3_OPERATIONS


class API_CRUD_FILES:
  def __init__(self):
    """Initialize the API_CRUD_FILES class

    Args:
        s3CrudFiles (S3_OPERATIONS): db reference to the where the files are stored
        dbCrudS3IDs (DB_CRUD_S3IDS): db reference to where all the file's informations are stored
        dbCrudMaterial (DB_CRUD_MATERIAL): db reference to the material table
    """
    self.__s3CrudFiles = S3_OPERATIONS('thinkup-files')
    self.__dbCrudS3Ids = setup.startSetup('S3-IDs')
    self.__dbCrudMaterial = setup.startSetup('Materials')

  def __add_file_to_material(self, idOfTheFile: str, idOfTheMaterial: str):
    """Adds file to a specific material

    Args:
        idOfTheFile (str): id of the file you want to add to the material
        idOfTheMaterial (str): id of the material you want to add the file to

    Returns:
        _type_: response
    """
    materialJson = self.__dbCrudMaterial.getMaterial(idOfTheMaterial)
    
    materialJson['files'].append(idOfTheFile)
    return self.__dbCrudMaterial.updateMaterial(idOfTheMaterial, materialJson)
    

  def add_file(self, id: str, file, materialId: str, isAddedWithMaterial: bool):
    """Add file to dynamoDB and S3; dynamoDB is used to store the file's information and S3 is used to store the file's content

    Args:
        id (str): id of the file
        file (file): the file itself
        materialId (str): id of the material the file belongs to
        isAddedWithMaterial (bool): True => the file has been added on material creation, False => the file has been added after the material was created

    Returns:
        _type_: response
    """
    file_copy = file
    file_copy.seek(0, os.SEEK_END)
    file_size = file_copy.tell()

    file_extension = pathlib.Path(file.filename).suffix
    pathname, extension = os.path.splitext(file.filename)
    file_type2 = file.content_type
    file.seek(0)

    fileObj = File(id, file_size, pathname, file_extension, file_type2, materialId)
    self.__dbCrudS3Ids.addId(IdEncoder.toJson(fileObj))

    if not isAddedWithMaterial:
      self.__add_file_to_material(id, materialId)

    return self.__s3CrudFiles.Upload(fileObj, file, False)

  def download_file(self, idOfTheFile: str):
    """Get the file from S3 and send it to the client with it's initial name (not the name of the file used to store it in S3)

    Args:
        idOfTheFile (str): id of the file you want to download

    Returns:
        file: the file you want to download
    """
    mType = self.__dbCrudS3Ids.getDetails(idOfTheFile)
    dw_file = self.__s3CrudFiles.Download(idOfTheFile, mType['extension'])
    fName = mType['name'] + mType['extension']

    return send_file(
        dw_file['Body'],
        as_attachment=True,
        attachment_filename=fName,
        mimetype=mType['file_type'],
      )

  def delete_file(self, idOfTheFile: str, isDirect):
    """Deletes a file from a material

    Args:
        idOfTheFile (str): id of the file you want to delete
        isDirect (bool): _description_

    Returns:
        _type_: response
    """
    fileJson = self.__dbCrudS3Ids.getDetails(idOfTheFile)

    # Delete from dynamoDB
    self.__dbCrudS3Ids.delete_id(idOfTheFile)

    # Delete from S3
    self.__s3CrudFiles.Delete(idOfTheFile, fileJson['extension'])

    # Update Material
    if isDirect:
      materialJson = self.__dbCrudMaterial.getMaterial(fileJson['materialId'])
      materialJson['files'].remove(idOfTheFile)

      return self.__dbCrudMaterial.updateMaterial(idOfTheFile, materialJson)
    return "ok"

  def getDetails(self, id: str):
    return self.__dbCrudS3Ids.getDetails(id)
   


