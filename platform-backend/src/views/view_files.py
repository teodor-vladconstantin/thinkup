from api.api_crud_files import API_CRUD_FILES
from api.api_crud_materials import API_CRUD_MATERIALS
from api.api_crud_projects import API_CRUD_PROJECTS
from api.api_track_activity import updateActivity
from dynamoDB import setup
from flask import Blueprint, request, send_from_directory, abort
import os
from s3.s3_crud import S3_OPERATIONS, is_image
from utils.jwt_server import require_auth, current_user_id, is_project_member

urlFiles = Blueprint('view_files', __name__)

apiFiles = API_CRUD_FILES()
apiProjects = API_CRUD_PROJECTS()
apiMaterial = API_CRUD_MATERIALS(apiProjects, apiFiles)


def _is_material_owner(materialId, user_id):
    """A file belongs to a material, which belongs to a project - check
    ownership through that chain."""
    material = apiMaterial.get_material(materialId)
    if not material or "ErrorMessage" in material:
        return False
    project = apiProjects.getProject(material.get('projectId'))
    return is_project_member(project, user_id)

@urlFiles.route('/storage/<string:bucket>/<string:filename>', methods=['GET'])
def get_local_file(bucket, filename):
    ALLOWED_BUCKETS = [
        'thinkup-profile-picture',
        'thinkup-user-cover-images',
        'thinkup-open-school',
        'thinkup-thumbnail',
        'thinkup-files',
        'thinkup-logos',
        'thinkup-gallery'
    ]
    if bucket not in ALLOWED_BUCKETS:
        return "Invalid Bucket", 403
        
    storage_path = os.path.join(os.getcwd(), 'local_storage', bucket)
    response = send_from_directory(storage_path, filename)
    # Uploads are served from the app's own origin: never let one run as a page (stored XSS).
    # sandbox = no scripts, opaque origin; nosniff = browser can't reinterpret the type.
    response.headers['Content-Security-Policy'] = "default-src 'none'; img-src 'self'; style-src 'unsafe-inline'; sandbox"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    if not is_image(filename):
        response.headers['Content-Disposition'] = 'attachment'
    return response

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

    if not _is_material_owner(materialId, current_user_id()):
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

    if not _is_material_owner(fileJson.get('materialId'), current_user_id()):
        abort(403, description="You are not authorized to delete this file")

    return apiFiles.delete_file(id, True)
