import uuid
from datetime import datetime

from flask import Blueprint, request, jsonify, abort
from utils.jwt_server import require_auth, current_user_id, require_mentor
from utils.logger import setup_logger
from dynamoDB import setup
from model.entity.warning import Warning
from model.entity.jsonencoders.warning_encoder import WarningEncoder

logger = setup_logger(__name__)

urlWarnings = Blueprint('view_warnings', __name__)

dbCrudWarnings = setup.startSetup('Warnings')


@urlWarnings.route('/warnings/<string:student_id>', methods=['POST'])
@require_auth()
def addWarning(student_id: str):
    """Issue a warning to a student

    Body:
        text (str): the warning message

    Args:
        student_id (str): id of the student being warned

    Returns:
        _type_: response
    """
    require_mentor()
    text = (request.json or {}).get('text')
    if not text:
        abort(400, description="text is required")

    warning_id = uuid.uuid4().hex
    warningObj = Warning(warning_id, student_id, current_user_id(), text, datetime.now().isoformat())
    result = dbCrudWarnings.addWarning(WarningEncoder.toJSON(warningObj))

    logger.info(f"Warning {warning_id} issued to student {student_id} by mentor {current_user_id()}")
    return result


@urlWarnings.route('/warnings/student/<string:student_id>', methods=['GET'])
@require_auth()
def get_student_warnings(student_id: str):
    """Get all warnings for a student. Only the student themself or a mentor can see them.

    Args:
        student_id (str): id of the student

    Returns:
        JSON: {"warnings": [...]}
    """
    if student_id != current_user_id():
        require_mentor()
    studentWarnings = [w for w in dbCrudWarnings.fullscanWarning() if w.get('studentId') == student_id]
    return jsonify({"warnings": studentWarnings})


@urlWarnings.route('/warnings/<string:id>', methods=['DELETE'])
@require_auth()
def deleteWarning(id: str):
    """Delete a warning (mentors only)

    Args:
        id (str): id of the warning to delete

    Returns:
        _type_: response
    """
    warning = dbCrudWarnings.getWarning(id)
    if not warning or "ErrorMessage" in warning:
        abort(404, description="Warning not found")
    require_mentor()

    result = dbCrudWarnings.deleteWarning(id)
    logger.info(f"Warning {id} deleted by {current_user_id()}")
    return result
