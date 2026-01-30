from model.entity.users.student import Student
from model.permissions.permissions import Permissions
from model.settings.settings import Settings


class Sponsor(Student):
    def __init__(self, id: str, name: str, email: str, description: str, settings: Settings, perms: Permissions):
        Student.__init__(id, name, email, description, settings, perms)
