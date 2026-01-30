import json

from api.api_crud_projects import API_CRUD_PROJECTS
from api.api_track_activity import updateActivity
from flask import Blueprint, request
from model.entity.goals.goals import Goals
from model.entity.materials.materials import Materials
from model.entity.project import Project
from model.entity.reviews.project_reviews import ProjectReviews
from utils.utils import Utils

urlProject = Blueprint('views', __name__)


apiProjects = API_CRUD_PROJECTS()

mentor_feedback = []

@urlProject.route('/projects/<string:id>', methods=['GET'])
def getProject(id: str):
    """Get a project

    Args:
        id (str): id of the project

    Returns:
        JSON: JSON of the project
    """
    print(f"DEBUG: getProject called with id={id}, args={request.args}")
    try:
        result = apiProjects.getProject(id)
        print(f"DEBUG: getProject result={result}")
        return result
    except Exception as e:
        print(f"DEBUG: getProject EXCEPTION: {e}")
        return {"ErrorMessage": str(e)}, 500

@urlProject.route('/projects/<string:id>', methods=['DELETE'])
def deleteProject(id: str):
    """Delete a project

    Args:
        id (str): id of the project to delete

    Returns:
        _type_: response
    """
    return apiProjects.deleteProject(id)

@urlProject.route('/projects/<string:id>', methods=['POST'])
@Utils.check_project_token
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
    projectReviews = ProjectReviews(projectJson['id'], 0, 0, [])
    projectObj = Project(projectJson['id'], projectJson['name'], str(projectJson['name']).lower(), projectJson['description'], "defaultThumbnailCIVIC1", ".png", projectJson['created_by'], [projectJson['created_by']], projectJson['creation_date'], projectJson['area_of_implementation'], goal, materials_obj, "pitchId#999", {"accept_reviews": True}, projectReviews, mentor_feedback)

    creatorID = projectJson['created_by']
    updateActivity(creatorID, "create_project", 2)

    return apiProjects.addProject(project_token, projectObj)
    
@urlProject.route('/projects/<string:id>', methods=['PUT'])
def updateProject(id: str):
    """Update a project

    Args:
        id (str): id of the project to update

    Returns:
        _type_: response
    """
    projectJson = request.form.get('json')
    projectJson = json.loads(projectJson)

    projectJson["created_by"] = apiProjects.getProject(id)["createdBy"]
    try:
        thumbnail = request.files['file']
    except KeyError:
        thumbnail = None

    projectUpdated = apiProjects.getProject(id)

    creatorID = projectJson['created_by']
    updateActivity(creatorID,'edit_project')

    return apiProjects.updateProject(projectUpdated, projectJson, thumbnail)


@urlProject.route('/projects', methods=['GET'])
def get_all_projects():
    """Get all projects

    Returns:
        list: all the projects
    """
    filter = None
    try:
        filter = request.args['filter']
    except KeyError as err:
        print(err)

    return apiProjects.getAllProjects(filter)

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
