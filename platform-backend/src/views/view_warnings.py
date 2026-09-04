import uuid
from datetime import datetime

from flask import Blueprint, request, jsonify, abort
from utils.jwt_server import require_auth
from utils.logger import setup_logger
from dynamoDB import setup
from model.entity.warning import Warning
from model.entity.jsonencoders.warning_encoder import WarningEncoder

logger = setup_logger(__name__)

urlWarnings = Blueprint('view_warnings', __name__)

dbCrudWarnings = setup.startSetup('Warnings')
dbCrudUsers = setup.startSetup('Users')


@urlWarnings.route('/warnings/<string:student_id>', methods=['POST'])
@require_auth()
def addWarning(student_id: str):
    """Issue a warning to a student

    Body:
        mentorId (str): id of the mentor issuing the warning (must resolve to a Mentor user)
        text (str): the warning message

    Args:
        student_id (str): id of the student being warned

    Returns:
        _type_: response
    """
    try:
        warningJson = request.json
        if not warningJson:
            abort(400, description="Missing JSON body")

        mentor_id = warningJson.get('mentorId')
        if not mentor_id:
            abort(400, description="mentorId is required")

        mentor = dbCrudUsers.getUser(mentor_id)
        if not mentor or "ErrorMessage" in mentor:
            logger.warning(f"Warning issue attempt by unknown user {mentor_id}")
            abort(403, description="You are not authorized to issue warnings")

        if mentor.get('role') != 'Mentor':
            logger.warning(f"Warning issue attempt by non-mentor user {mentor_id} (role={mentor.get('role')})")
            abort(403, description="Only mentors can issue warnings")

        text = warningJson.get('text')
        if not text:
            abort(400, description="text is required")

        warning_id = uuid.uuid4().hex
        issuedDate = datetime.now().isoformat()

        warningObj = Warning(warning_id, student_id, mentor_id, text, issuedDate)
        result = dbCrudWarnings.addWarning(WarningEncoder.toJSON(warningObj))

        logger.info(f"Warning {warning_id} issued to student {student_id} by mentor {mentor_id}")
        return result
    except KeyError as e:
        logger.warning(f"Missing field issuing warning for student {student_id}: {e}")
        return jsonify({"error": f"Missing field: {str(e)}"}), 400
    except Exception as e:
        from werkzeug.exceptions import HTTPException
        if isinstance(e, HTTPException):
            raise e
        logger.error(f"Error issuing warning for student {student_id}: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@urlWarnings.route('/warnings/student/<string:student_id>', methods=['GET'])
def get_student_warnings(student_id: str):
    """Get all warnings for a student

    Args:
        student_id (str): id of the student

    Returns:
        JSON: {"warnings": [...]}
    """
    logger.info(f"get_student_warnings called with student_id={student_id}")
    try:
        allWarnings = dbCrudWarnings.fullscanWarning()
        studentWarnings = [w for w in allWarnings if w.get('studentId') == student_id]
        return jsonify({"warnings": studentWarnings})
    except Exception as e:
        logger.error(f"Error listing warnings for student {student_id}: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@urlWarnings.route('/warnings/<string:id>', methods=['DELETE'])
@require_auth()
def deleteWarning(id: str):
    """Delete a warning

    Args:
        id (str): id of the warning to delete

    Returns:
        _type_: response
    """
    logger.info(f"Attempting to delete warning {id}")
    try:
        warning = dbCrudWarnings.getWarning(id)
        if not warning or "ErrorMessage" in warning:
            abort(404, description="Warning not found")

        result = dbCrudWarnings.deleteWarning(id)
        logger.info(f"Warning {id} deleted successfully")
        return result
    except Exception as e:
        from werkzeug.exceptions import HTTPException
        if isinstance(e, HTTPException):
            raise e
        logger.error(f"Error deleting warning {id}: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500
