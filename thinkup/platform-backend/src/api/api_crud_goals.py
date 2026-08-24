from dynamoDB import setup
from dynamoDB.db_crud_goals import DB_CRUD_GOALS
from model.entity.goals.goal import Goal
from model.entity.goals.goals import Goals
from model.entity.jsonencoders.goal_encoder import GoalEncoder
from s3.s3_crud import S3_OPERATIONS

from api.api_crud_projects import API_CRUD_PROJECTS


class API_CRUD_GOALS:
    def __init__(self, db_crud_goals: DB_CRUD_GOALS):
      """Initialize the API_CRUD_GOALS class

      Args:
          db_crud_goals (DB_CRUD_GOALS): db reference to the goals table
      """
      self.__db_crud_goals = db_crud_goals
      self.__apiProj = API_CRUD_PROJECTS()

    def getGoal(self, idOfTheGoal: str):
      """Get a goal from the database

      Args:
          idOfTheGoal (str): id of the goal

      Returns:
          JSON: JSON of the goal
      """
      return self.__db_crud_goals.getGoal(idOfTheGoal)

    def addGoal(self, goalObject: Goal):
      """Add a goal to the database

      Args:
          goalObject (Goal): goal object to be added to the database

      Returns:
          _type_: response
      """
      # Add to project
      projJson = self.__apiProj.getProject(goalObject.get_projectId())
      projJson2 = projJson
      projJson['goals'].insert(0, goalObject.get_id())

      # Update Project
      self.__apiProj.updateProject(projJson2, projJson, None)

      # Add goal to database
      return self.__db_crud_goals.addGoal(GoalEncoder.toJson(goalObject))

    def updateGoal(self, goalJson: dict):
      """Update a goal in the database

      Args:
          goalJson (dict): goal json to be updated in the database

      Returns:
          _type_: response
      """
      return self.__db_crud_goals.updateGoal(goalJson)

    def deleteGoal(self, idOfGoal: str):
      """Delete a goal from the database

      Args:
          idOfGoal (str): id of the goal to be deleted

      Returns:
          _type_: response
      """
      goalJson = self.getGoal(idOfGoal)
      projJson = self.__apiProj.getProject(goalJson['projectId'])
      projJson2 = projJson

      # Remove from project
      projJson['goals'].remove(idOfGoal)
      self.__apiProj.updateProject(projJson2, projJson, None)

      # Delete goal from database
      return self.__db_crud_goals.deleteGoal(idOfGoal)

