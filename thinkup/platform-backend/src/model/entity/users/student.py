from model.entity.awards.awards import Awards
from model.entity.goals.personal_objective import PersonalObjective
from model.permissions.permissions import Permissions
from model.puzzle.puzzle import Puzzle
from model.settings.settings import Settings


class Student:
    def __init__(self, id: str, name: str, search_term: str, profile_picture: str, profile_picture_extension: str, cover_picture: str, cover_picture_extension: str,
                 email: str, description: str, settings: Settings, perms: Permissions, activity, puzzle: Puzzle, personal_objectives: list,
                 social_connections: dict, awards: Awards, fav_files: list):


        self.__id = id
        self.__name = name
        self.__search_term = search_term
        self.__profile_picture = profile_picture
        self.__profile_picture_extension = profile_picture_extension
        self.__cover_picture = cover_picture
        self.__cover_picture_extension = cover_picture_extension
        self.__email = email
        self.__description = description
        self.__settings = settings
        self.__perms = perms
        self.__activity = activity
        self.__puzzle = puzzle
        self.__personal_objectives = personal_objectives
        self.__social_connections = social_connections
        self.__awards = awards
        self.__fav_files = fav_files

    def get_favFiles(self):
        return self.__fav_files
        
    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_search_term(self):
        return self.__search_term

    def set_name(self, new_name: str):
        self.__name = new_name
    
    def get_email(self):
        return self.__email

    def get_description(self):
        return self.__description

    def set_description(self, new_description: str):
        self.__description = new_description

    def get_settings(self):
        return self.__settings
        
    def set_settings(self, new_settings: Settings):
        self.__settings = new_settings

    def get_perms(self):
        return self.__perms

    def get_profile_picture(self):
        return self.__profile_picture

    def get_profile_picture_extension(self):
        return self.__profile_picture_extension

    def get_cover_picture(self):
        return self.__cover_picture

    def set_cover_picture(self, cover_picture):
        self.__cover_picture = cover_picture

    def get_cover_picture_extension(self):
        return self.__cover_picture_extension

    def set_cover_picture_extension(self, cover_picture_extension):
        self.__cover_picture_extension = cover_picture_extension

    def get_activity(self):
        return self.__activity

    def set_activity(self, new_activity: dict):
        self.__activity = new_activity

    def get_puzzle(self):
        return self.__puzzle

    def set_puzzle(self, new_puzzle: Puzzle):
        self.__puzzle = new_puzzle

    def get_personal_objectives(self):
        return self.__personal_objectives

    def get_social_connections(self):
        return self.__social_connections

    def get_awards(self):
        return self.__awards

    def set_awards(self, new_awards: Puzzle):
        self.__awards = new_awards

    def get_fav_files(self):
        return self.__fav_files

    def set_fav_files(self, fav_files):
        self.__fav_files = fav_files

    def __str__(self):
        return "name: {0}, profile picture: {1}, email: {2}".format(self.get_name(), self.get_profile_picture(), self.get_email())
