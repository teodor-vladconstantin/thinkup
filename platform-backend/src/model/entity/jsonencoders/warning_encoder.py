from ..warning import Warning


class WarningEncoder():
  def toJSON(o):
    if isinstance(o, Warning):
      Item = {
        'id': o.get_id(),
        'studentId': o.get_studentId(),
        'issuedBy': o.get_issuedBy(),
        'text': o.get_text(),
        'issuedDate': o.get_issuedDate(),
      }
      return Item
    return None


# USE : WarningEncoder().toJSON(warning)

"""
JSON Format :

{
    "id": "a1b2c3d4",
    "studentId": "studentUserId",
    "issuedBy": "mentorUserId",
    "text": "Nu ai trimis proiectul la timp",
    "issuedDate": "2026-09-04T12:00:00"
}
"""
