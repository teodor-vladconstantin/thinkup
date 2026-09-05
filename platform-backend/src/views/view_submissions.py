from datetime import datetime
from decimal import Decimal

from flask import Blueprint, request, jsonify, abort
from utils.jwt_server import require_auth, current_user_id
from utils.logger import setup_logger
from dynamoDB import setup
from model.entity.submission import Submission
from model.entity.jsonencoders.submission_encoder import SubmissionEncoder

logger = setup_logger(__name__)

urlSubmissions = Blueprint('view_submissions', __name__)

dbCrudSubmissions = setup.startSetup('Submissions')
dbCrudUsers = setup.startSetup('Users')
dbCrudProjects = setup.startSetup('Projects')


def _num(value):
    """Convert a DynamoDB Decimal to a plain JSON-serializable number"""
    if isinstance(value, Decimal):
        return float(value) if value % 1 else int(value)
    return value


def _serializable(submission: dict):
    return {k: _num(v) for k, v in submission.items()}


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
    try:
        gradeJson = request.json
        if not gradeJson:
            abort(400, description="Missing JSON body")

        mentor_id = current_user_id()

        mentor = dbCrudUsers.getUser(mentor_id)
        if not mentor or "ErrorMessage" in mentor:
            logger.warning(f"Grading attempt by unknown user {mentor_id}")
            abort(403, description="You are not authorized to grade submissions")

        if mentor.get('role') != 'Mentor':
            logger.warning(f"Grading attempt by non-mentor user {mentor_id} (role={mentor.get('role')})")
            abort(403, description="Only mentors can grade submissions")

        score = Decimal(str(gradeJson['score']))
        feedback = gradeJson.get('feedback')
        gradedDate = datetime.now().isoformat()
        submission_id = f"{challenge_id}#{student_id}"

        submissionObj = Submission(submission_id, student_id, challenge_id, score, mentor_id, gradedDate, feedback)
        submissionDict = SubmissionEncoder.toJSON(submissionObj)

        existing = dbCrudSubmissions.getSubmission(submission_id)
        if "ErrorMessage" in existing:
            result = dbCrudSubmissions.addSubmission(submissionDict)
        else:
            result = dbCrudSubmissions.updateSubmission(submissionDict)

        logger.info(f"Submission {submission_id} graded by mentor {mentor_id}")
        return result
    except KeyError as e:
        logger.warning(f"Missing field grading submission {challenge_id}/{student_id}: {e}")
        return jsonify({"error": f"Missing field: {str(e)}"}), 400
    except Exception as e:
        from werkzeug.exceptions import HTTPException
        if isinstance(e, HTTPException):
            raise e
        logger.error(f"Error grading submission {challenge_id}/{student_id}: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


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
    try:
        gradeJson = request.json
        if not gradeJson:
            abort(400, description="Missing JSON body")

        mentor_id = current_user_id()

        mentor = dbCrudUsers.getUser(mentor_id)
        if not mentor or "ErrorMessage" in mentor:
            logger.warning(f"Grading attempt by unknown user {mentor_id}")
            abort(403, description="You are not authorized to grade submissions")

        if mentor.get('role') != 'Mentor':
            logger.warning(f"Grading attempt by non-mentor user {mentor_id} (role={mentor.get('role')})")
            abort(403, description="Only mentors can grade submissions")

        project = dbCrudProjects.getProject(project_id)
        if not project or "ErrorMessage" in project:
            abort(404, description="Project not found")

        challenge_id = project.get('challengeId')
        if not challenge_id:
            abort(400, description="This project has no challenge assigned")

        score = Decimal(str(gradeJson['score']))
        feedback = gradeJson.get('feedback')
        gradedDate = datetime.now().isoformat()

        results = []
        for admin_id in project.get('adminList', []):
            submission_id = f"{challenge_id}#{admin_id}"
            submissionObj = Submission(submission_id, admin_id, challenge_id, score, mentor_id, gradedDate, feedback, project_id)
            submissionDict = SubmissionEncoder.toJSON(submissionObj)

            existing = dbCrudSubmissions.getSubmission(submission_id)
            if "ErrorMessage" in existing:
                result = dbCrudSubmissions.addSubmission(submissionDict)
            else:
                result = dbCrudSubmissions.updateSubmission(submissionDict)
            results.append(_serializable(submissionDict))

        logger.info(f"Project {project_id} graded by mentor {mentor_id}, {len(results)} submission(s)")
        return jsonify({"submissions": results})
    except KeyError as e:
        logger.warning(f"Missing field grading project {project_id}: {e}")
        return jsonify({"error": f"Missing field: {str(e)}"}), 400
    except Exception as e:
        from werkzeug.exceptions import HTTPException
        if isinstance(e, HTTPException):
            raise e
        logger.error(f"Error grading project {project_id}: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@urlSubmissions.route('/submissions/student/<string:student_id>', methods=['GET'])
def get_student_submissions(student_id: str):
    """Get all submissions for a student, with a computed total score

    Args:
        student_id (str): id of the student

    Returns:
        JSON: {"submissions": [...], "totalScore": number}
    """
    logger.info(f"get_student_submissions called with student_id={student_id}")
    try:
        allSubmissions = dbCrudSubmissions.fullscanSubmission()
        studentSubmissions = [
            _serializable(s) for s in allSubmissions if s.get('studentId') == student_id
        ]
        totalScore = sum(s.get('score', 0) or 0 for s in studentSubmissions)
        return jsonify({"submissions": studentSubmissions, "totalScore": totalScore})
    except Exception as e:
        logger.error(f"Error listing submissions for student {student_id}: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@urlSubmissions.route('/submissions/challenge/<string:challenge_id>', methods=['GET'])
def get_challenge_submissions(challenge_id: str):
    """Get all submissions for a challenge

    Args:
        challenge_id (str): id of the challenge

    Returns:
        JSON: {"submissions": [...]}
    """
    logger.info(f"get_challenge_submissions called with challenge_id={challenge_id}")
    try:
        allSubmissions = dbCrudSubmissions.fullscanSubmission()
        challengeSubmissions = [
            _serializable(s) for s in allSubmissions if s.get('challengeId') == challenge_id
        ]
        return jsonify({"submissions": challengeSubmissions})
    except Exception as e:
        logger.error(f"Error listing submissions for challenge {challenge_id}: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500
