import json
from dynamoDB import setup
from dynamoDB.db_crud_material import DB_CRUD_MATERIAL
from model.entity.jsonencoders.material_encoder import MaterialEncoder
from model.entity.materials.material import Material

from api.api_crud_files import API_CRUD_FILES
from api.api_crud_projects import API_CRUD_PROJECTS


class API_CRUD_MATERIALS:
  def __init__(self, apiCrudProjects: API_CRUD_PROJECTS, apiCrudFiles: API_CRUD_FILES):
    """Initialize the API_CRUD_MATERIALS class.

    Args:
        apiCrudProjects (API_CRUD_PROJECTS): API_CRUD_PROJECTS reference
        apiCrudFiles (API_CRUD_FILES): API_CRUD_FILES object
        db_crud_materials (DB_CRUD_MATERIAL): db reference to the materials table 
    """
    self.__apiCrudProjects = apiCrudProjects
    self.__apiCrudFiles = apiCrudFiles
    self.__db_crud_materials = setup.startSetup('Materials')

  def get_material(self, idOfTheMaterial: str):
    """Get a material from the database

    Args:
        idOfTheMaterial (str): id of the material

    Returns:
        JSON: JSON of the material
    """
    return self.__db_crud_materials.getMaterial(idOfTheMaterial)

  def add_material(self, idOfTheMaterial: str, materialJson: dict, materialFiles: list):
    """Add a material to the database

    Args:
        idOfTheMaterial (str): id of the material
        materialJson (dict): JSON of the material
        materialFiles (list): files to be added to the material

    Returns:
        _type_: response
    """
    # Take each file and assign it it's id from the materialJson
    for (file, idOfTheFile) in zip(materialFiles, materialJson["files"]):
      self.__apiCrudFiles.add_file(idOfTheFile, file, idOfTheMaterial, True)
    materialObj = Material(idOfTheMaterial, materialJson['name'], materialJson['projectId'], materialJson['description'], materialJson['creationDate'], materialJson['createdBy'], materialJson['files'])

    projectUpdated = self.__apiCrudProjects.getProject(materialJson['projectId'])
    projectJson = projectUpdated
    projectJson['materials'].append(materialObj.get_id())

    # Update project
    self.__apiCrudProjects.updateProject(projectUpdated, projectJson, None)


    return  self.__db_crud_materials.addMaterial(MaterialEncoder.toJSON(materialObj))

  def update_material(self, materialId :str,updatedMaterialJSON:dict):
    """Update a material in the database
    
    Args:
        materialId (str): the id of the material to be updated
        updatedMaterialJSON (dict): the newly upated material attributes

    Returns:
        _type_: response
    """
    return self.__db_crud_materials.updateMaterial(materialId,updatedMaterialJSON)

  def delete_material(self, idOfTheMaterial: str):
    """Delete a material from the database

    Args:
        idOfTheMaterial (str): id of the material

    Returns:
        _type_: response
    """
    materialJson = self.get_material(idOfTheMaterial)
    try:
      for fileId in materialJson['files']:
        self.__apiCrudFiles.delete_file(fileId, False)
    except KeyError as e:
      pass

    # Update project
    projJSON = self.__apiCrudProjects.getProject(materialJson['projectId'])
    projJSON2 = projJSON
    projJSON['materials'].remove(idOfTheMaterial)
    self.__apiCrudProjects.updateProject(projJSON2, projJSON, None)
    
    return self.__db_crud_materials.deleteMaterial(idOfTheMaterial)

  def move_material(self, idOfTheMaterial: str, upOrDown: int):
    """Move a material up/down in the list of materials

    Args:
        idOfTheMaterial (str): id of the material
        upOrDown (int): 1 for up, -1 for down

    Returns:
        _type_: response
    """

    materialJSON = self.get_material(idOfTheMaterial)
    projectJSON = self.__apiCrudProjects.getProject(materialJSON["projectId"])
    tempProject = projectJSON

    materials_list = projectJSON["materials"]

    materialIndex = materials_list.index(idOfTheMaterial)

    if (materialIndex == 0 and upOrDown == 1) or (materialIndex == len(materials_list) - 1 and upOrDown == -1):
      return "not possible"

    materials_list[materialIndex], materials_list[materialIndex - upOrDown] = materials_list[materialIndex - upOrDown], materials_list[materialIndex]

    tempProject["materials"] = materials_list

    return self.__apiCrudProjects.updateProject(projectJSON, tempProject, None)
