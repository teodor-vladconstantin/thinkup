from model.entity.users.mentor import Mentor
from model.permissions.permissions import Permissions
from model.settings.settings import Settings


class Tech (Mentor):
    def __init__(self, id: str, name: str, email: str, description: str, settings: Settings, perms: Permissions, project):
        super().__init__(id, name, email, description, settings, perms, project)
