import json

from flask import Blueprint, request, jsonify, abort
from utils.jwt_server import require_auth, current_user_id
from utils.logger import setup_logger
from dynamoDB import setup
from model.entity.challenge import Challenge
from model.entity.jsonencoders.challenge_encoder import ChallengeEncoder

logger = setup_logger(__name__)

urlChallenges = Blueprint('view_challenges', __name__)

dbCrudChallenges = setup.startSetup('Challenges')
dbCrudUsers = setup.startSetup('Users')
dbCrudProjects = setup.startSetup('Projects')


def _require_mentor(user_id):
    """Abort with 403 unless user_id resolves to a User with role Mentor."""
    if not user_id:
        abort(403, description="created_by is required")
    user = dbCrudUsers.getUser(user_id)
    if not user or "ErrorMessage" in user:
        abort(403, description="You are not authorized to manage challenges")
    if user.get('role') != 'Mentor':
        abort(403, description="Only mentors can manage challenges")


@urlChallenges.route('/challenges/<string:id>', methods=['GET'])
def getChallenge(id: str):
    """Get a challenge

    Args:
        id (str): id of the challenge

    Returns:
        JSON: JSON of the challenge
    """
    logger.info(f"getChallenge called with id={id}")
    try:
        result = dbCrudChallenges.getChallenge(id)
        logger.info(f"getChallenge result={result}")
        return result
    except Exception as e:
        logger.error(f"getChallenge EXCEPTION: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@urlChallenges.route('/challenges/<string:id>', methods=['DELETE'])
@require_auth()
def deleteChallenge(id: str):
    """Delete a challenge

    Args:
        id (str): id of the challenge to delete

    Returns:
        _type_: response
    """
    logger.info(f"Attempting to delete challenge {id}")
    try:
        challenge = dbCrudChallenges.getChallenge(id)
        if not challenge or "ErrorMessage" in challenge:
            logger.warning(f"Challenge {id} not found for deletion")
            abort(404, description="Challenge not found")

        user_id = current_user_id()
        logger.info(f"User {user_id} requesting deletion of challenge {id}")

        _require_mentor(user_id)

        is_creator = challenge.get('createdBy') == user_id

        if not is_creator:
            logger.warning(f"User {user_id} unauthorized to delete challenge {id}")
            abort(403, description="You are not authorized to delete this challenge")

        referencing_projects = [
            p for p in dbCrudProjects.fullscanProject()
            if p.get('challengeId') == id
        ]
        if referencing_projects:
            logger.warning(f"Refusing to delete challenge {id}: {len(referencing_projects)} project(s) reference it")
            abort(409, description=f"Cannot delete: {len(referencing_projects)} project(s) reference this challenge")

        result = dbCrudChallenges.deleteChallenge(id)
        logger.info(f"Challenge {id} deleted successfully")
        return result
    except Exception as e:
        from werkzeug.exceptions import HTTPException
        if isinstance(e, HTTPException):
            raise e
        logger.error(f"Error deleting challenge {id}: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@urlChallenges.route('/challenges/<string:id>', methods=['POST'])
@require_auth()
def addChallenge(id: str):
    """Add a challenge

    Args:
        id (str): id of the challenge to add

    Returns:
        _type_: response
    """
    try:
        challengeJson = request.json
        _require_mentor(challengeJson.get('created_by'))
        challengeObj = Challenge(
            id,
            challengeJson['name'],
            challengeJson['description'],
            challengeJson['deadline'],
            challengeJson['maxScore'],
            challengeJson['created_by'],
            challengeJson['creation_date']
        )

        result = dbCrudChallenges.addChallenge(ChallengeEncoder.toJSON(challengeObj))
        logger.info(f"Challenge {id} created")
        return result
    except KeyError as e:
        logger.warning(f"Missing field creating challenge {id}: {e}")
        return jsonify({"error": f"Missing field: {str(e)}"}), 400
    except Exception as e:
        from werkzeug.exceptions import HTTPException
        if isinstance(e, HTTPException):
            raise e
        logger.error(f"Error creating challenge {id}: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@urlChallenges.route('/challenges/<string:id>', methods=['PUT'])
@require_auth()
def updateChallenge(id: str):
    """Update a challenge

    Args:
        id (str): id of the challenge to update

    Returns:
        _type_: response
    """
    logger.info(f"Attempting to update challenge {id}")
    try:
        challengeJson = request.json
        if not challengeJson:
            abort(400, description="Missing JSON body")

        challengeUpdated = dbCrudChallenges.getChallenge(id)
        if not challengeUpdated or "ErrorMessage" in challengeUpdated:
            abort(404, description="Challenge not found")

        user_id = current_user_id()
        _require_mentor(user_id)

        is_creator = challengeUpdated.get('createdBy') == user_id

        if not is_creator:
            logger.warning(f"User {user_id} unauthorized to update challenge {id}")
            abort(403, description="You are not authorized to update this challenge")

        for field in ('name', 'description', 'deadline', 'maxScore'):
            if field in challengeJson:
                challengeUpdated[field] = challengeJson[field]

        result = dbCrudChallenges.updateChallenge(challengeUpdated)
        logger.info(f"Challenge {id} updated successfully")
        return result
    except Exception as e:
        from werkzeug.exceptions import HTTPException
        if isinstance(e, HTTPException):
            raise e
        logger.error(f"Error updating challenge {id}: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@urlChallenges.route('/challenges', methods=['GET'])
def get_all_challenges():
    """Get all challenges

    Returns:
        list: all the challenges
    """
    try:
        result = dbCrudChallenges.fullscanChallenge()
        return jsonify({"challenges": result})
    except Exception as e:
        logger.error(f"Error listing challenges: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500
