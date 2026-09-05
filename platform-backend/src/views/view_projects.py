import json

from flask import Blueprint, request, jsonify, abort
from utils.jwt_server import require_auth
from utils.logger import setup_logger
from api.api_crud_projects import API_CRUD_PROJECTS
from api.api_track_activity import updateActivity
from model.entity.goals.goals import Goals
from model.entity.materials.materials import Materials
from model.entity.project import Project
from model.entity.reviews.project_reviews import ProjectReviews
from utils.utils import Utils
from utils.jwt_server import require_auth
from utils.logger import setup_logger
from flask import jsonify

logger = setup_logger(__name__)

urlProject = Blueprint('views', __name__)


apiProjects = API_CRUD_PROJECTS()

logger = setup_logger(__name__)

mentor_feedback = []

@urlProject.route('/projects/<string:id>', methods=['GET'])
def getProject(id: str):
    """Get a project

    Args:
        id (str): id of the project

    Returns:
        JSON: JSON of the project
    """
    logger.info(f"getProject called with id={id}, args={request.args}")
    try:
        result = apiProjects.getProject(id)
        logger.info(f"getProject result={result}")
        return result
    except Exception as e:
        logger.error(f"getProject EXCEPTION: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@urlProject.route('/projects/<string:id>', methods=['DELETE'])
@require_auth(None)
def deleteProject(id: str):
    """Delete a project

    Args:
        id (str): id of the project to delete

    Returns:
        _type_: response
    """
    logger.info(f"Attempting to delete project {id}")
    try:
        project = apiProjects.getProject(id)
        if not project:
             logger.warning(f"Project {id} not found for deletion")
             abort(404, description="Project not found")

        # Authorization check: the JWT is a service-to-service (M2M) token, it does
        # not identify the calling user, so current_token.sub never identifies the
        # actual caller. We trust the user id the client supplies instead (same
        # precedent as PUT /projects/<id>).
        deleteJson = request.get_json(silent=True) or {}
        user_id = deleteJson.get('created_by')
        logger.info(f"User {user_id} requesting deletion of project {id}")
        
        is_owner = project.get('createdBy') == user_id
        is_admin = user_id in project.get('adminList', [])
        
        if not (is_owner or is_admin):
            logger.warning(f"User {user_id} unauthorized to delete project {id}")
            abort(403, description="You are not authorized to delete this project")

        result = apiProjects.deleteProject(id)
        logger.info(f"Project {id} deleted successfully")
        return result
    except Exception as e:
        # If abort is raised, re-raise it so Flask handles it
        if isinstance(e,  (int, str, dict)): # Just in case abort raises something weird, though usually it raises HTTPException
             pass
        # Actually abort raises HTTPException which inherits from Exception. 
        # But we want to catch generic errors. 
        # Check if it is an HTTPException
        from werkzeug.exceptions import HTTPException
        if isinstance(e, HTTPException):
            raise e
        logger.error(f"Error deleting project {id}: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@urlProject.route('/projects/<string:id>', methods=['POST'])
@require_auth(None)
# @Utils.check_project_token  # disabled: project creation no longer requires a token
def addProject(id: str):
    """Add a project

    Args:
        id (str): id of the project to add

    Returns:
        _type_: response
    """
    project_token = request.args.get('project_token')
    materials_obj = Materials([])
    goal = Goals([])
    projectJson = request.json

    created_by = projectJson['created_by']
    challenge_id = projectJson['challengeId']

    existing_projects = apiProjects.getOwnedProjects(created_by).get('projects', [])
    if any(p.get('challengeId') == challenge_id for p in existing_projects):
        abort(409, description="Ai deja un proiect pe acest challenge")

    projectReviews = ProjectReviews(projectJson['id'], 0, 0, [])
    projectObj = Project(projectJson['id'], projectJson['name'], str(projectJson['name']).lower(), projectJson['description'], "defaultThumbnailCIVIC1", ".png", created_by, [created_by], projectJson['creation_date'], challenge_id, goal, materials_obj, "pitchId#999", {"accept_reviews": True}, projectReviews, mentor_feedback, [])

    updateActivity(created_by, "create_project", 2)

    return apiProjects.addProject(project_token, projectObj)
@urlProject.route('/projects/<string:id>', methods=['PUT'])
@require_auth(None)
def updateProject(id: str):
    """Update a project

    Args:
        id (str): id of the project to update

    Returns:
        _type_: response
    """
    logger.info(f"Attempting to update project {id}")
    projectJsonRaw = request.form.get('json')
    if not projectJsonRaw:
         abort(400, description="Missing 'json' form data")

    projectJson = json.loads(projectJsonRaw)

    # Fetch existing project
    projectUpdated = apiProjects.getProject(id)
    if not projectUpdated:
         abort(404, description="Project not found")

    # Authorization check. Requests reach Flask with a service-to-service (M2M)
    # token, not a per-user one, so current_token.sub never identifies the
    # actual caller - it's the same constant for everybody. We trust the user
    # id the client supplies instead (same precedent as the Submissions grading
    # endpoint's mentorId check).
    user_id = projectJson.get('created_by')
    is_owner = projectUpdated.get('createdBy') == user_id
    is_admin = user_id in projectUpdated.get('adminList', [])

    if not (is_owner or is_admin):
         logger.warning(f"User {user_id} unauthorized to update project {id}")
         abort(403, description="You are not authorized to update this project")

    new_challenge_id = projectJson.get('challengeId')
    if new_challenge_id and new_challenge_id != projectUpdated.get('challengeId'):
        existing_projects = apiProjects.getOwnedProjects(user_id).get('projects', [])
        if any(p.get('challengeId') == new_challenge_id and p.get('id') != id for p in existing_projects):
            abort(409, description="Ai deja un proiect pe acest challenge")
    
    projectJson["created_by"] = projectUpdated["createdBy"]
    
    try:
        thumbnail = request.files['file']
    except KeyError:
        thumbnail = None

    creatorID = projectJson['created_by']
    updateActivity(creatorID,'edit_project')

    return apiProjects.updateProject(projectUpdated, projectJson, thumbnail)


@urlProject.route('/projects', methods=['GET'])
def get_all_projects():
    """Get all projects

    Returns:
        list: all the projects
    """
    return apiProjects.getAllProjects()

@urlProject.route('/user_projects/<string:id>', methods=['GET'])
def get_user_projects(id: str):
    """Get all projects created by a user

    Args:
        id (str): id of the user

    Returns:
        list: list of all projects
    """
    return apiProjects.getOwnedProjects(id)


@urlProject.route('/projects/search/<string:name>', methods=['GET'])
def search_project(name: str):
    """Search for a project by name

    Args:
        name (str): name of the project

    Returns:
        list: projects matching the name
    """
    return apiProjects.searchProject(name)

@urlProject.route('/projects/<string:id>/accept_reviews/<int:accept>', methods=['PUT'])
@require_auth(None)
def accept_reviews(id: str, accept: int):
    """Accept or reject reviews for a project

    Args:
        id (str): id of the project
        accept (int): 1 => accept, 0 => reject

    Returns:
        _type_: _description_
    """
    projectJson = apiProjects.getProject(id)
    projJson2 = projectJson

    if accept in [0, 1] and bool(accept) != projJson2["settings"]["accept_reviews"]:
        projectJson["settings"]["accept_reviews"] = bool(accept)
        return apiProjects.updateProject(projJson2, projectJson, None)

    return "Nothing to update"

@urlProject.route('/projects/<string:id>/admins/<string:adminId>', methods=['DELETE'])
@require_auth(None)
def delete_admin(id: str, adminId: int):
    """Delete an admin from a project

    Args:
        id (str): id of the project
        adminId (int): id of the admin to delete

    Returns:
        _type_: response
    """
    projectJson = apiProjects.getProject(id)
    projJson2 = apiProjects.getProject(id)

    if len(projJson2["adminList"]) <= 1:
        return "Cannot have less than 1 admin"

    projJson2["adminList"].remove(adminId)
    
    projectJson["adminList"] = []
    return apiProjects.updateProject(projJson2, projectJson, None)
