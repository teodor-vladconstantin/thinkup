from decimal import Decimal
from functools import wraps

from api.api_crud_projects import API_CRUD_PROJECTS
from flask import make_response, request

apiProj = API_CRUD_PROJECTS()


class Utils:
  @staticmethod
  def check_project_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
      project_token = request.args.get('project_token')
      if apiProj.isTokenValid(project_token):
        return f(*args, **kwargs)
      return make_response("Project token is required", 400)
    return decorated
  
  @staticmethod
  def update_average_rating(old_average, old_count, rating, sign=1):
    """Running mean after adding (sign=1) or removing (sign=-1) one rating.

    Returns Decimal - boto3 rejects floats.
    """
    old_average, old_count, rating = (Decimal(str(x)) for x in (old_average, old_count, rating))
    new_count = old_count + sign
    if new_count <= 0:
      return Decimal(0)
    return (old_average * old_count + sign * rating) / new_count
      


if __name__ == "__main__":
  u = Utils.update_average_rating
  assert u(0, 0, 4) == 4
  assert u(4, 1, 2) == 3
  assert u(3, 2, 5) == Decimal(11) / 3
  assert u(3, 2, 2, -1) == 4
  assert u(4, 1, 4, -1) == 0
  print("ok")
