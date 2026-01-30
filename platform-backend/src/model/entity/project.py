import string

from model.entity.goals.goals import Goals
from model.entity.materials.materials import Materials
from model.entity.mentor_feedback.mentor_feedback import MENTOR_FEEDBACK
from model.entity.reviews.project_reviews import ProjectReviews


class Project:
    def __init__(self, id: str, name: str, searchTerm: str, description: str, thumbnail, thumbnail_extension,
                 createdBy: str, adminList: list, creationDate, areaOfImplementation: str, goals: Goals,
                 materials: Materials, pitchId: str, settings: dict, projectReviews: ProjectReviews, mentor_feedback: list):
        self.__id = id
        self.__name = name
        self.__searchTerm = searchTerm
        self.__createdBy = createdBy
        self.__description = description
        self.__thumbnail = thumbnail
        self.__thumbnail_extension = thumbnail_extension
        self.__creationDate = creationDate
        self.__areaOfImplementation = areaOfImplementation
        self.__goals = goals
        self.__materials = materials
        self.__pitchId = pitchId
        self.__adminList = adminList
        self.__settings = settings
        self.__projectReviews = projectReviews
        self.__mentor_feedback = mentor_feedback

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def set_name(self, name: string):
        self.__name = name

    def get_description(self):
        return self.__description

    def set_description(self, description: string):
        self.__description = description

    def get_thumbnail(self):
        return self.__thumbnail

    def set_thumbnail(self, thumbnail):
        self.__thumbnail = thumbnail

    def get_thumbnail_extension(self):
        return self.__thumbnail_extension

    def get_creationDate(self):
        return self.__creationDate

    def get_areOfImplementation(self):
        return self.__areaOfImplementation

    def set_areOfImplementation(self, areOfImplementation: string):
        self.__areaOfImplementation = areOfImplementation

    def get_goals(self):
        return self.__goals

    def set_goals(self, goals: Goals):
        self.__goals = goals

    def get_materials(self):
        return self.__materials

    def get_pitchId(self):
        return self.__pitchId

    def set_pitchId(self, pitchId):
        self.__pitchId = pitchId

    def get_searchTerm(self):
        return self.__searchTerm

    def get_createdBy(self):
        return self.__createdBy

    def get_adminList(self):
        return self.__adminList

    def add_admin(self, admin):
        self.__adminList.append(admin)

    def get_settings(self):
        return self.__settings

    def get_projectReviews(self):
        return self.__projectReviews

    def set_projectReviews(self, projectReviews):
        self.__projectReviews = projectReviews

    def get_mentor_feedback(self):
        return self.__mentor_feedback

    def set_projectReviews(self, mentor_feedback):
        self.__mentor_feedback = mentor_feedback
