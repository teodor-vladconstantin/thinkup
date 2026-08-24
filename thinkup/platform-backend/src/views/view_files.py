from api.api_crud_files import API_CRUD_FILES
from api.api_track_activity import updateActivity
from dynamoDB import setup
from flask import Blueprint, request, send_from_directory
import os
from s3.s3_crud import S3_OPERATIONS
from utils.jwt_server import require_auth

urlFiles = Blueprint('view_files', __name__)

apiFiles = API_CRUD_FILES()

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
    materialId = fileJson['id']
    return apiFiles.delete_file(id, materialId, True)
