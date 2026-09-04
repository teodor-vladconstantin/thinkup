import json

from flask import Blueprint, request, jsonify, abort
from utils.jwt_server import require_auth
from utils.logger import setup_logger
from dynamoDB import setup
from model.entity.challenge import Challenge
from model.entity.jsonencoders.challenge_encoder import ChallengeEncoder

logger = setup_logger(__name__)

urlChallenges = Blueprint('view_challenges', __name__)

dbCrudChallenges = setup.startSetup('Challenges')


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

        # Authorization check: same precedent as PUT /projects/<id> - the JWT is a
        # service-to-service (M2M) token and does not identify the calling user, so
        # we trust the user id the client supplies instead of current_token.sub.
        deleteJson = request.get_json(silent=True) or {}
        user_id = deleteJson.get('created_by')
        logger.info(f"User {user_id} requesting deletion of challenge {id}")

        is_creator = challenge.get('createdBy') == user_id

        if not is_creator:
            logger.warning(f"User {user_id} unauthorized to delete challenge {id}")
            abort(403, description="You are not authorized to delete this challenge")

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

        # Authorization check: same precedent as PUT /projects/<id> - trust the
        # user id the client supplies instead of current_token.sub (M2M token).
        user_id = challengeJson.get('created_by')
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
