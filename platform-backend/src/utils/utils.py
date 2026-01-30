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
  def get_average_rating(new_rating: float, old_rating: float):
    return new_rating if old_rating == 0 else (old_rating + new_rating) / 2 
      
