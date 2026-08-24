import json
from datetime import date

from api.api_crud_mentor_feedback import API_CRUD_MENTOR_FEEDBACK
from api.api_crud_users import API_CRUD_USERS
from api.api_track_activity import updateActivity
from dynamoDB import setup
from flask import Blueprint, request
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


@urlUser.route('/users/<string:id>', methods=['POST'])
def postUser(id: str):
    """Post a user to database

    Args:
        id (str): id of the user

    Returns:
        _type_: response
    """
    userJson = request.json
    search_term = userJson["name"]
    search_term.replace("-", " ")

    userObj = None

    if userJson['email'][userJson['email'].index('@') + 1 :] == "mentor.think-up.academy":
        userObj = Mentor(userJson['id'], userJson['name'], search_term.lower(), "default", ".png", "default", ".png",
                      userJson['email'], userJson['description'],
                      settings, permissions, activity, puzzle, personal_objectives, {}, awards, fav_files)
    else:
        userObj = Student(userJson['id'], userJson['name'], search_term.lower(), "default", ".png", "default", ".png",
                      userJson['email'], userJson['description'],
                      settings, permissions, activity, puzzle, personal_objectives, {}, awards, fav_files)

    temp_return =apiUsers.addUser(userObj)
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
    return apiUsers.getUser(id)


@urlUser.route('/users/<string:id>', methods=['DELETE'])
def deleteUser(id: str):
    """Delete a user from database

    Args:
        id (str): id of the user to delete

    Returns:
        _type_: response
    """
    return apiUsers.deleteUser(id)


@urlUser.route('/users/<string:id>', methods=['PUT'])
def updateUser(id: str):
    """Update a user from database

      Args:
        id (str): id of the user to update

    Returns:
        _type_: response
    """
    userJson = request.form.get('json')
    userJson = json.loads(userJson)

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
def givePieceToUser(id):
    """Give a puzzle piece to a user

    Args:
        id (str): id of the user

    Returns:
        _type_: response
    """
    userJson = apiUsers.getUser(id)
    try:
        piece_id = request.form.get('piece_id')
    except KeyError:
        piece_id = None

    return apiUsers.addPuzzlePiece(userJson, piece_id)


@urlUser.route('/users/<string:id>/changeLanguage/<string:lang>', methods=['PUT'])
def changeLanguage(id: str, lang: str):
    """Change the language of a user's interface
    Args:
        id (str): id of the user
        lang (str): en / ro
    Returns:
        _type_: response
    """
    accepted_languages = ["en", "ro"]

    userJson = apiUsers.getUser(id)
    userUpdated = userJson

    if lang in accepted_languages and lang != userJson['settings']['language']:
        userJson['settings']['language'] = lang
        return apiUsers.updateUser(userUpdated, userJson, None, None)

    return "Language not accepted"


@urlUser.route('/users/<string:id>/social/<string:social_platform>', methods=['PUT'])
def addSocial(id: str, social_platform: str):
    """Add a social platform to a user's profile
    Args:
        id (str): id of the user
        social_platform (str): one of the accepted social platforms
    Returns:
        _type_: response
    """
    accepted_social_platforms = ["facebook", "instagram", "github"]
    link = request.args.get('link')

    userJson = apiUsers.getUser(id)
    userUpdated = userJson
    
    updateActivity(id,"add_social")
    
    userUpdated['social_connections'][social_platform] = link

    return apiUsers.updateUser(userUpdated, userJson, None, None)


@urlUser.route('/users/<string:id>/social/<string:social_platform>', methods=['DELETE'])
def deleteSocial(id: str, social_platform: str):
    """Add a social platform to a user's profile
    Args:
        id (str): id of the user
        social_platform (str): one of the accepted social platforms
    Returns:
        _type_: response
    """
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

    currentYear = str(date.today().year)

    for key, item in userActivity.items():
        if currentYear - int(key.split('-')[0]) == 1:
            newUserActivity[key] = item

    return newUserActivity

@urlUser.route('/users/favFiles/<string:id>', methods=['POST'])
def updateFavFiles(id):
    """Adds a file to users favorites
    Args    
        id: file name
        userId: the user that saved the file as favorite

    """
    print(request.form)
    userJson = request.form.get("json")
    userJson = json.loads(userJson)
    userId = userJson['userId']
    updateActivity(userId,'mark_favorite_file')
    return apiUsers.addFavFile(userId, id)

@urlUser.route('/users/favFiles/<string:id>', methods=['DELETE'])
def removeFavFiles(id):
    """removes a file from users favorites
    Args    
        id: file name
        userId: the user that saved the file as favorite

    """
    print(request.form)
    userJson = request.form.get("json")
    userJson = json.loads(userJson)
    userId = userJson['userId']
    return apiUsers.removeFavFile(userId, id)

@urlUser.route('/users/favFiles/<string:id>', methods=['GET'])
def showFavFiles(id):
    return apiUsers.showFavFile(id)
