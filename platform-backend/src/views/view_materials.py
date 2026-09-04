import json

from api.api_crud_files import API_CRUD_FILES
from api.api_crud_materials import API_CRUD_MATERIALS
from api.api_crud_projects import API_CRUD_PROJECTS
from api.api_track_activity import updateActivity
from flask import Blueprint, request, abort
from utils.jwt_server import require_auth

urlMaterial = Blueprint('views', __name__)

apiFiles = API_CRUD_FILES()

apiProjects = API_CRUD_PROJECTS()

apiMaterial = API_CRUD_MATERIALS(apiProjects, apiFiles)


def _is_project_owner(project, user_id):
  """Check if user_id is the creator or an admin of the given project dict.

  Note: user_id is a value the client supplies (see PUT /projects/<id> for
  why - the JWT is a service-to-service M2M token, not per-user).
  """
  if not project or "ErrorMessage" in project or not user_id:
    return False
  return project.get('createdBy') == user_id or user_id in project.get('adminList', [])


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

  project = apiProjects.getProject(materialJson.get('projectId'))
  if not _is_project_owner(project, materialJson.get('createdBy')):
    abort(403, description="You are not authorized to add materials to this project")

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

  existingMaterial = apiMaterial.get_material(id)
  if not existingMaterial or "ErrorMessage" in existingMaterial:
    abort(404, description="Material not found")

  project = apiProjects.getProject(existingMaterial.get('projectId'))
  if not _is_project_owner(project, materialJson.get('updatedBy')):
    abort(403, description="You are not authorized to update this material")

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
  if not materialJson or "ErrorMessage" in materialJson:
    abort(404, description="Material not found")

  deleteJson = request.get_json(silent=True) or {}
  project = apiProjects.getProject(materialJson.get('projectId'))
  if not _is_project_owner(project, deleteJson.get('created_by')):
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

