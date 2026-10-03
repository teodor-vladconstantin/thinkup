from flask import Blueprint, request, jsonify, abort
from utils.jwt_server import require_auth, current_user_id, require_mentor
from utils.logger import setup_logger
from dynamoDB import setup
from model.entity.challenge import Challenge
from model.entity.jsonencoders.challenge_encoder import ChallengeEncoder

logger = setup_logger(__name__)

urlChallenges = Blueprint('view_challenges', __name__)

dbCrudChallenges = setup.startSetup('Challenges')
dbCrudProjects = setup.startSetup('Projects')


def _require_own_challenge(id):
    """Return the challenge, or abort unless the caller is the mentor who created it."""
    challenge = dbCrudChallenges.getChallenge(id)
    if not challenge or "ErrorMessage" in challenge:
        abort(404, description="Challenge not found")
    require_mentor()
    if challenge.get('createdBy') != current_user_id():
        abort(403, description="You are not authorized to modify this challenge")
    return challenge


@urlChallenges.route('/challenges/<string:id>', methods=['GET'])
def getChallenge(id: str):
    """Get a challenge

    Args:
        id (str): id of the challenge

    Returns:
        JSON: JSON of the challenge
    """
    return dbCrudChallenges.getChallenge(id)


@urlChallenges.route('/challenges/<string:id>', methods=['DELETE'])
@require_auth()
def deleteChallenge(id: str):
    """Delete a challenge

    Args:
        id (str): id of the challenge to delete

    Returns:
        _type_: response
    """
    _require_own_challenge(id)

    referencing_projects = [
        p for p in dbCrudProjects.fullscanProject()
        if p.get('challengeId') == id
    ]
    if referencing_projects:
        abort(409, description=f"Nu se poate șterge: {len(referencing_projects)} proiect(e) folosesc acest challenge")

    result = dbCrudChallenges.deleteChallenge(id)
    logger.info(f"Challenge {id} deleted by {current_user_id()}")
    return result


@urlChallenges.route('/challenges/<string:id>', methods=['POST'])
@require_auth()
def addChallenge(id: str):
    """Add a challenge

    Args:
        id (str): id of the challenge to add

    Returns:
        _type_: response
    """
    require_mentor()
    challengeJson = request.json
    challengeObj = Challenge(
        id,
        challengeJson['name'],
        challengeJson['description'],
        challengeJson['deadline'],
        challengeJson['maxScore'],
        current_user_id(),
        challengeJson['creation_date']
    )

    result = dbCrudChallenges.addChallenge(ChallengeEncoder.toJSON(challengeObj))
    logger.info(f"Challenge {id} created")
    return result


@urlChallenges.route('/challenges/<string:id>', methods=['PUT'])
@require_auth()
def updateChallenge(id: str):
    """Update a challenge

    Args:
        id (str): id of the challenge to update

    Returns:
        _type_: response
    """
    challengeJson = request.json
    if not challengeJson:
        abort(400, description="Missing JSON body")

    challengeUpdated = _require_own_challenge(id)
    for field in ('name', 'description', 'deadline', 'maxScore'):
        if field in challengeJson:
            challengeUpdated[field] = challengeJson[field]

    result = dbCrudChallenges.updateChallenge(challengeUpdated)
    logger.info(f"Challenge {id} updated")
    return result


@urlChallenges.route('/challenges', methods=['GET'])
def get_all_challenges():
    """Get all challenges

    Returns:
        list: all the challenges
    """
    return jsonify({"challenges": dbCrudChallenges.fullscanChallenge()})
