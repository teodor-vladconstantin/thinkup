from model.entity.project import Project
from model.entity.users.student import Student
from model.permissions.permissions import Permissions
from model.settings.settings import Settings

class Competitor(Student):
    def __init__(self, id: str, name: str, email: str, description: str, settings: Settings, perms: Permissions, projects: list, activity: dict):
        super().__init__(id, name, email, description, settings, perms, activity)
        self.__projects = projects

    def get_projects(self):
        return self.__projects

    def add_project(self, project_id):
        self.__projects.append(project_id)

    def remove_project(self, project_id):
        self.__projects.remove(project_id)