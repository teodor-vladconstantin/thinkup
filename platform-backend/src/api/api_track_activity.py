from datetime import date

from dynamoDB.setup import startSetup
from s3.s3_crud import S3_OPERATIONS

from api.api_crud_users import API_CRUD_USERS

import math

apiUsers = API_CRUD_USERS()

activityTypeMax={
    "non_spamable":math.inf,
    "edit_account":3, #added in view_users
    "create_project":1,
    "create_account": 1, #added in view_users
    "add_review": 1, #added in view_reviews
    "add_social":3, # added in view_users
    "add_material":5, #added in view_materials
    "remove_material":5, # added in view_materials
    "update_material":5, # didn't find in view
    "edit_project":3, #added in view_projects
    "mark_favorite_file":3, #added in view_users
    "download_file":3 #added in view_files
}

def updateActivity(id:str, activity_type:str="non_spamable", contor: int = 1):
    """Update the activity of a user
    Args:
        id(str): id of a user
        activity_type(str): the type of activity (spam prevention)
        contor(int): How many times to increment the activity (default 1)
    """
    userJson = apiUsers.getUser(idOfTheUser = id)
    updatedUser = userJson

    todayDate = str(date.today())

    userActivity = userJson['activity']  # we get the user's activity
    
    if(userActivity.get(todayDate)==None): #checks if there is a key for todays date
        userActivity.update({todayDate:{}}) #if not adds it
    
    if(userActivity[todayDate].get(activity_type)==None):#checks if there is a key for our activity type
        userActivity[todayDate].update({activity_type:0})#if not adds it

    
    if(userActivity[todayDate][activity_type]<activityTypeMax[activity_type]):#checks if reached the max amount of activites per day
        userActivity[todayDate][activity_type]+=contor#increments the activity by a certain amount
    
    updatedUser.update(userActivity)

    apiUsers.updateActivity(userJson, updatedUser)