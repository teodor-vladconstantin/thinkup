import os
import random
from flask import jsonify

from dynamoDB import setup
from dynamoDB.db_crud_users import DB_CRUD_USERS
from model.entity.jsonencoders.user_encoder import UserEncoder
from s3.s3_crud import S3_OPERATIONS


class API_CRUD_USERS:
    def __init__(self):
        """Initialize the API_CRUD_USERS class
        """
        self.__dbCrudUsers = setup.startSetup('Users')
        self.__s3ProfilePic = S3_OPERATIONS('thinkup-profile-picture')
        self.__s3CoverPic = S3_OPERATIONS('thinkup-user-cover-images')


    def getUser(self, idOfTheUser):
        """Get a user from database

        Args:
            idOfTheUser (str): id of the user

        Returns:
            dict: dictionary with the user
        """
        return self.__dbCrudUsers.getUser(idOfTheUser)

    def searchUsers(self, username: str):
        """Search for a specific user

        Args:
            username (str): username to search for

        Returns:
            list: list of all matching users
        """
        if username is None:
            return {"users":self.__dbCrudUsers.getAllUsers()}
        return {"users":self.__dbCrudUsers.searchUser(username)}

    def addUser(self, userObj):
        """Add a user to the database

        Args:
            userObj (User): user object

        Returns:
            _type_: response
        """
        return self.__dbCrudUsers.addUser(UserEncoder.toJSON(userObj))

    def updateUser(self, userUpdated, userJson, profilePic, coverPic):
        """Update a user in the database

        Args:
            userUpdated (dict): dictionary of user before update
            userJson (dict): updated attributes of the user
            profilePic (File or None): new profile picture or None

        Returns:
            _type_: response
        """
        deletePreviousProfilePicture = False
        deletePreviousCoverPicture = False
        previousProfileId = None
        previousCoverId = None

        try:
            userUpdated["name"] = userJson["name"]
            temp_username = userJson["name"]
            temp_username.replace('-', ' ')
            userUpdated["search_term"] = temp_username.lower()
        except KeyError:
            pass

        try:
            userUpdated["description"] = userJson["description"]
        except KeyError:
            pass

        try:
            userUpdated["mentor_feedback"] = userJson["mentor_feedback"]
        except KeyError:
            pass

        try:  # TODO: Remove this after frontend adds the personal_objectives field
            userUpdated["personal_objectives"] = userJson["personal_objectives"]
        except KeyError as e:
            userUpdated["personal_objectives"] = "NA"

        if coverPic is not None:
            if userUpdated["cover_picture"] != "default":
                deletePreviousCoverPicture = True
                previousCoverId = userUpdated["cover_picture"]
            userUpdated["cover_picture"] = userJson["cover_picture"]

            pathname, extension = os.path.splitext(coverPic.filename)
            new_name = userUpdated["cover_picture"] + extension

            self.__s3CoverPic.Upload(new_name, coverPic, False)
            # Delete past profile pic
            if deletePreviousCoverPicture is True:
                self.__s3CoverPic.Delete(previousCoverId, userUpdated["cover_picture_extension"])
            userUpdated["cover_picture_extension"] = extension

        if profilePic is not None:
            if userUpdated["profile_picture"] != "default":
                deletePreviousProfilePicture = True
                previousProfileId = userUpdated["profile_picture"]
            userUpdated["profile_picture"] = userJson["profile_picture"]

            pathname, extension = os.path.splitext(profilePic.filename)
            new_name = userUpdated["profile_picture"] + extension

            self.__s3ProfilePic.Upload(new_name, profilePic, False)
            # Delete past profile pic
            if deletePreviousProfilePicture is True:
                self.__s3ProfilePic.Delete(previousProfileId, userUpdated["profile_picture_extension"])
            userUpdated["profile_picture_extension"] = extension
        return self.__dbCrudUsers.updateUser(userUpdated)

    def updateActivity(self, userUpdated, userJson):
        """Update user's activity

        Args:
            userUpdated (dict): dictionary of user before update
            userJson (dict): updated attributes of the user

        Returns:
            _type_: response
        """
        userUpdated["activity"] = userJson["activity"]
        return self.__dbCrudUsers.updateUser(userUpdated)

    def deleteUser(self, idOfTheUser):
        """Delete a user from database

        Args:
            idOfTheUser (str): id of the user to delete

        Returns:
            _type_: response
        """
        return self.__dbCrudUsers.deleteUser(idOfTheUser)

    def addPuzzlePiece(self, userJson, piece_id):
        """Add a puzzle piece to a user

        Args:
            userJson (dict): initial user dictionary
            piece_id (str): id of the piece to add

        Returns:
            _type_: response
        """
        if piece_id is None:
            piece_id = random.choice(list(userJson["puzzle"]["missing_pieces_ids"]))
        resp = None
        try:
            userJson["puzzle"]["missing_pieces_ids"].remove(piece_id)
            userJson["puzzle"]["acquired_pieces_ids"].append(piece_id)
        except Exception as e:
            print(e)
            resp = "Piece not found"
        if resp is None:
            self.__dbCrudUsers.updateUser(userJson)
            return "OK"

    def addFavFile(self, userId, fileId):
        userJson = self.getUser(userId)
        editedJson = userJson
        editedJson["fav_files"].append(fileId)
        return self.updateUser(userJson, editedJson, None, None)
    
    def removeFavFile(self, userId, fileId):
        userJson = self.getUser(userId)
        editedJson = userJson
        editedJson["fav_files"].remove(fileId)
        return self.updateUser(userJson, editedJson, None, None)
    
    def showFavFile(self, userId):
        userJson = self.getUser(userId)
        favFilesList = userJson["fav_files"]
        response = {"fav_files": favFilesList}
        return jsonify(response)
