from api.api_crud_files import API_CRUD_FILES
from api.api_crud_materials import API_CRUD_MATERIALS
from api.api_crud_projects import API_CRUD_PROJECTS
from api.api_track_activity import updateActivity
from dynamoDB import setup
from flask import Blueprint, request, send_from_directory, abort
import os
from s3.s3_crud import S3_OPERATIONS
from utils.jwt_server import require_auth

urlFiles = Blueprint('view_files', __name__)

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


def _is_material_owner(materialId, user_id):
    """A file belongs to a material, which belongs to a project - check
    ownership through that chain."""
    material = apiMaterial.get_material(materialId)
    if not material or "ErrorMessage" in material:
        return False
    project = apiProjects.getProject(material.get('projectId'))
    return _is_project_owner(project, user_id)

@urlFiles.route('/storage/<string:bucket>/<string:filename>', methods=['GET'])
def get_local_file(bucket, filename):
    ALLOWED_BUCKETS = [
        'thinkup-profile-picture',
        'thinkup-user-cover-images',
        'thinkup-open-school',
        'thinkup-thumbnail',
        'thinkup-files',
        'thinkup-logos'
    ]
    if bucket not in ALLOWED_BUCKETS:
        return "Invalid Bucket", 403
        
    storage_path = os.path.join(os.getcwd(), 'local_storage', bucket)
    return send_from_directory(storage_path, filename)

@urlFiles.route('/files/<string:id>', methods=['POST'])
@require_auth()
def postFile(id: str):
    """Add a file to the database

    Args:
        id (str): id of the new file

    Returns:
        _type_: response
    """
    materialId = request.form.get('materialid')
    createdBy = request.form.get('created_by')

    if not _is_material_owner(materialId, createdBy):
        abort(403, description="You are not authorized to add files to this material")

    file = request.files['file']
    return apiFiles.add_file(id, file, materialId, False)

@urlFiles.route('/files/<string:id>', methods=['GET'])
@require_auth()
def getFile(id: str):
    """Get a file details from the database

    Args:
        id (str): id of the file

    Returns:
        details (str): details of the file
    """
    return apiFiles.getDetails(id)

@urlFiles.route('/files/<string:id>', methods=['DELETE'])
@require_auth()
def deleteFile(id: str):
    """Delete a file from the database

    Args:
        id (str): id of the file to be deleted

    Returns:
        _type_: response
    """
    fileJson = apiFiles.getDetails(id)
    if not fileJson or "ErrorMessage" in fileJson:
        abort(404, description="File not found")

    deleteJson = request.get_json(silent=True) or {}
    if not _is_material_owner(fileJson.get('materialId'), deleteJson.get('created_by')):
        abort(403, description="You are not authorized to delete this file")

    return apiFiles.delete_file(id, True)
