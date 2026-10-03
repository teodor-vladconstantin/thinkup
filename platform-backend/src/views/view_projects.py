import json

from flask import Blueprint, request, abort
from utils.jwt_server import require_auth, current_user_id, is_project_member, is_mentor
from utils.logger import setup_logger
from api.api_crud_projects import API_CRUD_PROJECTS
from api.api_track_activity import updateActivity
from dynamoDB import setup
from model.entity.goals.goals import Goals
from model.entity.materials.materials import Materials
from model.entity.project import Project
from model.entity.reviews.project_reviews import ProjectReviews

logger = setup_logger(__name__)

urlProject = Blueprint('views', __name__)

apiProjects = API_CRUD_PROJECTS()

mentor_feedback = []


def _strip_photos(result):
    """Public project routes must not leak photo URLs; only /projects_gallery returns them."""
    if isinstance(result, dict):
        result.pop('photos', None)
        for p in result.get('projects', []):
            p.pop('photos', None)
    return result


def _require_project_member(id):
    """Return the project, or abort 404/403 unless the caller is its creator or an admin."""
    project = apiProjects.getProject(id)
    if not project or "ErrorMessage" in project:
        abort(404, description="Project not found")
    if not is_project_member(project, current_user_id()):
        abort(403, description="You are not authorized to modify this project")
    return project


@urlProject.route('/projects/<string:id>', methods=['GET'])
def getProject(id: str):
    """Get a project

    Args:
        id (str): id of the project

    Returns:
        JSON: JSON of the project
    """
    return _strip_photos(apiProjects.getProject(id))


@urlProject.route('/projects/<string:id>', methods=['DELETE'])
@require_auth(None)
def deleteProject(id: str):
    """Delete a project

    Args:
        id (str): id of the project to delete

    Returns:
        _type_: response
    """
    _require_project_member(id)
    result = apiProjects.deleteProject(id)
    logger.info(f"Project {id} deleted by {current_user_id()}")
    return result


@urlProject.route('/projects/<string:id>', methods=['POST'])
@require_auth(None)
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

    created_by = current_user_id()
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
    projectJsonRaw = request.form.get('json')
    if not projectJsonRaw:
         abort(400, description="Missing 'json' form data")

    projectJson = json.loads(projectJsonRaw)

    projectUpdated = _require_project_member(id)
    user_id = current_user_id()

    new_challenge_id = projectJson.get('challengeId')
    if new_challenge_id and new_challenge_id != projectUpdated.get('challengeId'):
        existing_projects = apiProjects.getOwnedProjects(user_id).get('projects', [])
        if any(p.get('challengeId') == new_challenge_id and p.get('id') != id for p in existing_projects):
            abort(409, description="Ai deja un proiect pe acest challenge")
    
    projectJson["created_by"] = projectUpdated["createdBy"]
    # Ratings are only changed by the reviews API, never by the project owner
    projectJson.pop("projectReviews", None)

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
    return _strip_photos(apiProjects.getAllProjects())

@urlProject.route('/projects_gallery', methods=['GET'])
@require_auth()
def get_gallery_projects():
    """Projects for the photo gallery: mentors see all, others only projects they belong to."""
    user_id = current_user_id()
    projects = apiProjects.getAllProjects()
    if is_mentor(user_id):
        return projects
    projects['projects'] = [
        p for p in projects['projects']
        if is_project_member(p, user_id)
    ]
    return projects

@urlProject.route('/user_projects/<string:id>', methods=['GET'])
def get_user_projects(id: str):
    """Get all projects created by a user

    Args:
        id (str): id of the user

    Returns:
        list: list of all projects
    """
    return _strip_photos(apiProjects.getOwnedProjects(id))


@urlProject.route('/projects/search/<string:name>', methods=['GET'])
def search_project(name: str):
    """Search for a project by name

    Args:
        name (str): name of the project

    Returns:
        list: projects matching the name
    """
    return _strip_photos(apiProjects.searchProject(name))

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
    projectJson = _require_project_member(id)
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
    projectJson = _require_project_member(id)
    projJson2 = apiProjects.getProject(id)

    if len(projJson2["adminList"]) <= 1:
        return "Cannot have less than 1 admin"
    if adminId not in projJson2["adminList"]:
        abort(404, description="User is not an admin of this project")

    projJson2["adminList"].remove(adminId)
    
    projectJson["adminList"] = []
    return apiProjects.updateProject(projJson2, projectJson, None)
