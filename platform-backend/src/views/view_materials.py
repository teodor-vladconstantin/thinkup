import json

from api.api_crud_files import API_CRUD_FILES
from api.api_crud_materials import API_CRUD_MATERIALS
from api.api_crud_projects import API_CRUD_PROJECTS
from api.api_track_activity import updateActivity
from flask import Blueprint, request, abort
from utils.jwt_server import require_auth, current_user_id, is_project_member

urlMaterial = Blueprint('views', __name__)

apiFiles = API_CRUD_FILES()

apiProjects = API_CRUD_PROJECTS()

apiMaterial = API_CRUD_MATERIALS(apiProjects, apiFiles)


def _get_material_dict(id):
  """Fetch a material, or None if it doesn't exist."""
  material = apiMaterial.get_material(id)
  if not material or "ErrorMessage" in material:
    return None
  return material


def _require_material_owner(id):
  """Abort 404/403 unless the caller owns the material's project."""
  material = _get_material_dict(id)
  if not material:
    abort(404, description="Material not found")
  if not is_project_member(apiProjects.getProject(material.get('projectId')), current_user_id()):
    abort(403, description="You are not authorized to move this material")


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

  user_id = current_user_id()
  project = apiProjects.getProject(materialJson.get('projectId'))
  if not is_project_member(project, user_id):
    abort(403, description="You are not authorized to add materials to this project")

  materialJson['createdBy'] = user_id
  updateActivity(user_id,'add_material',2)
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

  existingMaterial = _get_material_dict(id)
  if not existingMaterial:
    abort(404, description="Material not found")

  user_id = current_user_id()
  project = apiProjects.getProject(existingMaterial.get('projectId'))
  if not is_project_member(project, user_id):
    abort(403, description="You are not authorized to update this material")

  updateActivity(user_id,'update_material',1)

  return apiMaterial.update_material(id,materialJson)
  
@urlMaterial.route('/materials/<string:id>', methods=['GET'])
def getMaterial(id: str):
  """Get a material from the database

  Args:
      id (str): id of the material

  Returns:
      _type_: response
  """
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
  materialJson = _get_material_dict(id)
  if not materialJson:
    abort(404, description="Material not found")

  project = apiProjects.getProject(materialJson.get('projectId'))
  if not is_project_member(project, current_user_id()):
    abort(403, description="You are not authorized to delete this material")

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
  _require_material_owner(id)
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
  _require_material_owner(id)
  return apiMaterial.move_material(id, -1)

