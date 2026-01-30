from dynamoDB import setup
from dynamoDB.db_crud_awards import DB_CRUD_AWARDS
from dynamoDB.db_crud_users import DB_CRUD_USERS
from model.entity.awards.award import Award
from model.entity.awards.awards import Awards
from model.entity.jsonencoders.award_encoder import AwardEncoder
from s3.s3_crud import S3_OPERATIONS

from api.api_crud_users import API_CRUD_USERS


class API_CRUD_AWARDS:
    def __init__(self, db_crud_awards: DB_CRUD_AWARDS):
        self.__db_crud_awards = db_crud_awards

        self.__db_crud_users = DB_CRUD_USERS()
        s3_prof_ops = S3_OPERATIONS()
        s3_cover_ops = S3_OPERATIONS()

        self.__api_users = API_CRUD_USERS(self.__db_crud_users, s3_prof_ops, s3_cover_ops)

    def get_award(self, idOfTheAward):
        return self.__db_crud_awards.get_award(idOfTheAward)

    def add_award(self, award: Award):
        userJson = self.__api_users.getUser(award.get_userId())
        userJson2 = userJson

        userJson['awards'].insert(0, award.get_id())

        self.__api_users.updateUser(userJson2, userJson, None, None)

        #TODO: encoder
        return self.__db_crud_awards.add_award(AwardEncoder.toJson(award))

    def update_award(self, awardJson):
        return self.__db_crud_awards.update_award(awardJson)

    def delete_award(self, idOfTheAward):
        awardJson = self.get_award(idOfTheAward)
        userJson = self.__api_users.getUser(awardJson['userId'])

        userJson2 = userJson
        userJson['awards'].remove(idOfTheAward)

        self.__api_users.updateUser(userJson2, userJson, None, None)

        return self.__db_crud_awards.delete_award(idOfTheAward)

