from model.entity.awards.awards import Awards
from model.entity.users.student import Student
from model.permissions.permissions import Permissions
from model.puzzle.puzzle import Puzzle
from model.settings.settings import Settings


class Mentor (Student):
    def __init__(self, id: str, name: str, search_term: str, profile_picture: str, profile_picture_extension: str, cover_picture: str, cover_picture_extension: str,
                 email: str, description: str, settings: Settings, perms: Permissions, activity, puzzle: Puzzle, personal_objectives: list,
                 social_connections: dict, awards: Awards, fav_files: list, is_mentor: bool):
        super().__init__(id, name, search_term, profile_picture, profile_picture_extension, cover_picture, cover_picture_extension, email, description, settings, perms, activity, puzzle, personal_objectives, social_connections, awards, fav_files, is_mentor)
    