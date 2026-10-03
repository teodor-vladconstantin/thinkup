import json
from datetime import date

from api.api_crud_mentor_feedback import API_CRUD_MENTOR_FEEDBACK
from api.api_crud_users import API_CRUD_USERS
from api.api_track_activity import updateActivity
from dynamoDB import setup
from flask import Blueprint, request, abort
from utils.jwt_server import require_auth, current_user_id, current_user_email, require_mentor
from model.entity.goals.goals import Goals
from model.entity.goals.personal_objective import PersonalObjective
from model.entity.users.mentor import Mentor
from model.entity.users.student import Student
from model.permissions.permissions import Permissions
from model.puzzle.puzzle import Puzzle
from model.settings.settings import Settings
from s3.s3_crud import S3_OPERATIONS

todayDate = str(date.today())

urlUser = Blueprint('views', __name__)

apiUsers = API_CRUD_USERS()

perms = {
    'canCreateProject': True,
    'canEditProject': True,
    'canDeleteProject': False
}

activity = {
}

settings = Settings("ro", True, False)
permissions = Permissions(perms)
puzzle = Puzzle("puzzleID1", set(), set(["1", "2", "3", "4", "5", "6", "7", "8", "9"]),
                set(["firstPiece", "secondPiece", "thirdPiece"]))

personal_objectives = []
awards = []

mentor_feedback = []

fav_files = []


def require_self(id: str):
    """Abort 403 unless the caller is the user being modified."""
    if id != current_user_id():
        abort(403, description="You can only modify your own account")


@urlUser.route('/users/<string:id>', methods=['POST'])
@require_auth()
def postUser(id: str):
    """Post a user to database

    Args:
        id (str): id of the user

    Returns:
        _type_: response
    """
    require_self(id)
    userJson = request.json
    userJson['id'] = id
    search_term = userJson["name"]
    search_term.replace("-", " ")

    # Mentor role is granted by email domain, so the email must come from Auth0, not the body
    verified_email = current_user_email()
    if verified_email:
        userJson['email'] = verified_email
    domain = verified_email.rsplit('@', 1)[-1] if verified_email else None

    userObj = None

    if domain == "mentor.think-up.academy":
        userObj = Mentor(userJson['id'], userJson['name'], search_term.lower(), "default", ".png", "default", ".png",
                      userJson['email'], userJson['description'],
                      settings, permissions, activity, puzzle, personal_objectives, {}, awards, fav_files)
    else:
        userObj = Student(userJson['id'], userJson['name'], search_term.lower(), "default", ".png", "default", ".png",
                      userJson['email'], userJson['description'],
                      settings, permissions, activity, puzzle, personal_objectives, {}, awards, fav_files)

    temp_return = apiUsers.addUser(userObj)
    if isinstance(temp_return, dict) and "ErrorMessage" in temp_return:
        abort(409, description=temp_return["ErrorMessage"])

    updateActivity(userJson['id'], "create_account")
    return temp_return


@urlUser.route('/users/<string:id>', methods=['GET'])
def getUser(id: str):
    """Get a user from database

    Args:
        id (str): id of the user

    Returns:
        dict: dictionary with the user
    """
    user = apiUsers.getUser(id)
    user.pop('email', None)
    return user


@urlUser.route('/users/<string:id>', methods=['DELETE'])
@require_auth()
def deleteUser(id: str):
    """Delete a user from database

    Args:
        id (str): id of the user to delete

    Returns:
        _type_: response
    """
    require_self(id)
    return apiUsers.deleteUser(id)


@urlUser.route('/users/<string:id>', methods=['PUT'])
@require_auth()
def updateUser(id: str):
    """Update a user from database

      Args:
        id (str): id of the user to update

    Returns:
        _type_: response
    """
    require_self(id)
    userJson = request.form.get('json')
    userJson = json.loads(userJson)
    userJson.pop('mentor_feedback', None)

    try:
        profilePic = request.files['file']
    except KeyError:
        profilePic = None

    try:
        coverPic = request.files['file2']
    except KeyError:
        coverPic = None

    updateActivity(id,'edit_account')
    userUpdated = apiUsers.getUser(id)
    return apiUsers.updateUser(userUpdated, userJson, profilePic, coverPic)


@urlUser.route('/users', methods=['GET'])
def searchUsers():
    """Get all users

    Args:

    Returns:
        _type_: response
    """
    username = request.args.get("username")
    return apiUsers.searchUsers(username)


@urlUser.route('/users/<string:id>/givePuzzlePiece', methods=['POST'])
@require_auth()
def givePieceToUser(id):
    """Give a puzzle piece to a user

    Args:
        id (str): id of the user

    Returns:
        _type_: response
    """
    require_mentor()
    userJson = apiUsers.getUser(id)
    try:
        piece_id = request.form.get('piece_id')
    except KeyError:
        piece_id = None

    return apiUsers.addPuzzlePiece(userJson, piece_id)


@urlUser.route('/users/<string:id>/changeLanguage/<string:lang>', methods=['PUT'])
@require_auth()
def changeLanguage(id: str, lang: str):
    """Change the language of a user's interface
    Args:
        id (str): id of the user
        lang (str): en / ro
    Returns:
        _type_: response
    """
    require_self(id)
    accepted_languages = ["en", "ro"]

    userJson = apiUsers.getUser(id)
    userUpdated = userJson

    if lang in accepted_languages and lang != userJson['settings']['language']:
        userJson['settings']['language'] = lang
        return apiUsers.updateUser(userUpdated, userJson, None, None)

    return "Language not accepted"


@urlUser.route('/users/<string:id>/social/<string:social_platform>', methods=['PUT'])
@require_auth()
def addSocial(id: str, social_platform: str):
    """Add a social platform to a user's profile
    Args:
        id (str): id of the user
        social_platform (str): one of the accepted social platforms
    Returns:
        _type_: response
    """
    require_self(id)
    accepted_social_platforms = ["facebook", "instagram", "linkedin", "twitter", "gitHub"]
    if social_platform not in accepted_social_platforms:
        abort(400, description="Social platform not accepted")
    link = (request.args.get('link') or '').strip()
    if '://' not in link:
        link = 'https://' + link
    # Profile page window.open()s this link - only allow web URLs, never javascript:
    if not link.lower().startswith(('https://', 'http://')):
        abort(400, description="Link must be an http(s) URL")

    userJson = apiUsers.getUser(id)
    userUpdated = userJson
    
    updateActivity(id,"add_social")
    
    userUpdated['social_connections'][social_platform] = link

    return apiUsers.updateUser(userUpdated, userJson, None, None)


@urlUser.route('/users/<string:id>/social/<string:social_platform>', methods=['DELETE'])
@require_auth()
def deleteSocial(id: str, social_platform: str):
    """Add a social platform to a user's profile
    Args:
        id (str): id of the user
        social_platform (str): one of the accepted social platforms
    Returns:
        _type_: response
    """
    require_self(id)
    accepted_social_platforms = ["facebook", "instagram", "github"]

    userJson = apiUsers.getUser(id)
    userUpdated = userJson

    userUpdated['social_connections'].pop(social_platform, None)

    return apiUsers.updateUser(userUpdated, userJson, None, None)


@urlUser.route('/users/useractivity/currentyear/<string:id>', methods=['GET'])
def GetUserActivityCurrent(id):
    userData = apiUsers.getUser(id)
    userActivity = userData['activity']

    currentYear = int(str(date.today().year))

    newUserActivity = {}

    for key, item in userActivity.items():
        if currentYear - int(key.split('-')[0]) == 0:
            newUserActivity[key] = item

    return newUserActivity


@urlUser.route('/users/useractivity/lastyear/<string:id>', methods=['GET'])
def GetUserActivityLast(id):
    userData = apiUsers.getUser(id)
    userActivity = userData['activity']

    newUserActivity = {}

    currentYear = date.today().year

    for key, item in userActivity.items():
        if currentYear - int(key.split('-')[0]) == 1:
            newUserActivity[key] = item

    return newUserActivity

@urlUser.route('/users/favFiles/<string:id>', methods=['POST'])
@require_auth()
def updateFavFiles(id):
    """Adds a file to users favorites
    Args    
        id: file name
        userId: the user that saved the file as favorite

    """
    userId = current_user_id()
    updateActivity(userId,'mark_favorite_file')
    return apiUsers.addFavFile(userId, id)

@urlUser.route('/users/favFiles/<string:id>', methods=['DELETE'])
@require_auth()
def removeFavFiles(id):
    """removes a file from users favorites
    Args    
        id: file name
        userId: the user that saved the file as favorite

    """
    userId = current_user_id()
    return apiUsers.removeFavFile(userId, id)

@urlUser.route('/users/favFiles/<string:id>', methods=['GET'])
def showFavFiles(id):
    return apiUsers.showFavFile(id)
