from datetime import datetime
from decimal import Decimal, InvalidOperation

from flask import Blueprint, request, jsonify, abort
from utils.jwt_server import require_auth, current_user_id, require_mentor
from utils.logger import setup_logger
from dynamoDB import setup
from model.entity.submission import Submission
from model.entity.jsonencoders.submission_encoder import SubmissionEncoder

logger = setup_logger(__name__)

urlSubmissions = Blueprint('view_submissions', __name__)

dbCrudSubmissions = setup.startSetup('Submissions')
dbCrudProjects = setup.startSetup('Projects')
dbCrudChallenges = setup.startSetup('Challenges')


def _num(value):
    """Convert a DynamoDB Decimal to a plain JSON-serializable number"""
    if isinstance(value, Decimal):
        return float(value) if value % 1 else int(value)
    return value


def _serializable(submission: dict):
    return {k: _num(v) for k, v in submission.items()}


def _valid_score(gradeJson, challenge_id):
    """Return the score as Decimal, or abort 400 unless 0 <= score <= the challenge's maxScore."""
    challenge = dbCrudChallenges.getChallenge(challenge_id)
    if not challenge or "ErrorMessage" in challenge:
        abort(404, description="Challenge not found")
    try:
        score = Decimal(str(gradeJson['score']))
        max_score = Decimal(str(challenge.get('maxScore')))
    except InvalidOperation:
        abort(400, description="score must be a number")
    if not 0 <= score <= max_score:
        abort(400, description=f"score must be between 0 and {max_score}")
    return score


def _save(submission_id, student_id, challenge_id, score, feedback, project_id=None):
    """Create or overwrite the grade of one student for one challenge."""
    submissionDict = SubmissionEncoder.toJSON(Submission(
        submission_id, student_id, challenge_id, score, current_user_id(),
        datetime.now().isoformat(), feedback, project_id))
    if "ErrorMessage" in dbCrudSubmissions.getSubmission(submission_id):
        result = dbCrudSubmissions.addSubmission(submissionDict)
    else:
        result = dbCrudSubmissions.updateSubmission(submissionDict)
    return submissionDict, result


@urlSubmissions.route('/submissions/<string:challenge_id>/<string:student_id>', methods=['POST'])
@require_auth()
def gradeSubmission(challenge_id: str, student_id: str):
    """Grade a student's submission for a challenge

    Body:
        score (number): the score granted
        feedback (str, optional): free-text feedback

    Args:
        challenge_id (str): id of the challenge being graded
        student_id (str): id of the student being graded

    Returns:
        _type_: response
    """
    require_mentor()
    gradeJson = request.json
    if not gradeJson:
        abort(400, description="Missing JSON body")

    score = _valid_score(gradeJson, challenge_id)
    submission_id = f"{challenge_id}#{student_id}"
    _, result = _save(submission_id, student_id, challenge_id, score, gradeJson.get('feedback'))

    logger.info(f"Submission {submission_id} graded by mentor {current_user_id()}")
    return result


@urlSubmissions.route('/submissions/project/<string:project_id>', methods=['POST'])
@require_auth()
def gradeProject(project_id: str):
    """Grade every admin of a project for the project's challenge

    Body:
        score (number): the score granted
        feedback (str, optional): free-text feedback

    Args:
        project_id (str): id of the project being graded

    Returns:
        _type_: response
    """
    require_mentor()
    gradeJson = request.json
    if not gradeJson:
        abort(400, description="Missing JSON body")

    project = dbCrudProjects.getProject(project_id)
    if not project or "ErrorMessage" in project:
        abort(404, description="Project not found")

    challenge_id = project.get('challengeId')
    if not challenge_id:
        abort(400, description="This project has no challenge assigned")

    score = _valid_score(gradeJson, challenge_id)

    results = []
    for admin_id in project.get('adminList', []):
        submissionDict, _ = _save(f"{challenge_id}#{admin_id}", admin_id, challenge_id, score,
                                  gradeJson.get('feedback'), project_id)
        results.append(_serializable(submissionDict))

    logger.info(f"Project {project_id} graded by mentor {current_user_id()}, {len(results)} submission(s)")
    return jsonify({"submissions": results})


@urlSubmissions.route('/submissions/student/<string:student_id>', methods=['GET'])
@require_auth()
def get_student_submissions(student_id: str):
    """Get all submissions for a student, with a computed total score.
    Only the student themself or a mentor can see them.

    Args:
        student_id (str): id of the student

    Returns:
        JSON: {"submissions": [...], "totalScore": number}
    """
    if student_id != current_user_id():
        require_mentor()
    studentSubmissions = [
        _serializable(s) for s in dbCrudSubmissions.fullscanSubmission() if s.get('studentId') == student_id
    ]
    totalScore = sum(s.get('score', 0) or 0 for s in studentSubmissions)
    return jsonify({"submissions": studentSubmissions, "totalScore": totalScore})


@urlSubmissions.route('/submissions/challenge/<string:challenge_id>', methods=['GET'])
@require_auth()
def get_challenge_submissions(challenge_id: str):
    """Get all submissions for a challenge (mentors only)

    Args:
        challenge_id (str): id of the challenge

    Returns:
        JSON: {"submissions": [...]}
    """
    require_mentor()
    challengeSubmissions = [
        _serializable(s) for s in dbCrudSubmissions.fullscanSubmission() if s.get('challengeId') == challenge_id
    ]
    return jsonify({"submissions": challengeSubmissions})
