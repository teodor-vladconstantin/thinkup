import json

from api.api_crud_files import API_CRUD_FILES
from api.api_crud_materials import API_CRUD_MATERIALS
from api.api_crud_projects import API_CRUD_PROJECTS
from api.api_track_activity import updateActivity
from flask import Blueprint, request
from utils.jwt_server import require_auth

urlMaterial = Blueprint('views', __name__)

apiFiles = API_CRUD_FILES()

apiProjects = API_CRUD_PROJECTS()

apiMaterial = API_CRUD_MATERIALS(apiProjects, apiFiles)


@urlMaterial.route('/materials/<string:id>', methods=['POST'])
@require_auth()
def addMaterial(id: str):
  """Add a material to the database

  Args:
      id (str): id of the material

  Returns:
      _type_: response
  """
  materialJson = request.form.get('json')
  materialJson = json.loads(materialJson)
  materialFiles = request.files.getlist('files')
  userID = materialJson['createdBy']
  updateActivity(userID,'add_material',2)
  return apiMaterial.add_material(id, materialJson, materialFiles)

@urlMaterial.route('/materials/<string:id>', methods=['PUT'])
@require_auth()
def updateMaterial(id: str):
  """Update a material from the database

  Args:
      id (str): id of the material

  Returns:
      _type_: response
  """
  materialJson = request.form.get('json')
  materialJson = json.loads(materialJson)

  userID = materialJson['updatedBy']
  updateActivity(userID,'update_material',1)
  
  return apiMaterial.update_material(id,materialJson)
  
@urlMaterial.route('/materials/<string:id>', methods=['GET'])
def getMaterial(id: str):
  """Get a material from the database

  Args:
      id (str): id of the material

  Returns:
      _type_: response
  """
  print("material:" + id)
  return apiMaterial.get_material(id)

@urlMaterial.route('/materials/<string:id>', methods=['DELETE'])
@require_auth()
def deleteMaterial(id: str):
  """Delete a material from the database

  Args:
      id (str): id of the material

  Returns:
      _type_: response
  """
  materialJson = apiMaterial.get_material(id)
  materialJson = json.loads(materialJson)
  userID = materialJson['createdBy']
  updateActivity(userID,'remove_material')
  return apiMaterial.delete_material(id)

@urlMaterial.route('/materials/move/up/<string:id>', methods=['GET'])
@require_auth()
def switchMaterialUP(id: str):
  """Pushes the material up in list by one position

  Args:
      id (str): id of the material

  Returns:
      _type_: response
  """
  return apiMaterial.move_material(id, 1)


@urlMaterial.route('/materials/move/down/<string:id>', methods=['GET'])
@require_auth()
def switchMaterialDOWN(id: str):
  """Pushes the material down in list by one position

  Args:
      id (str): id of the material

  Returns:
      _type_: response
  """
  return apiMaterial.move_material(id, -1)

