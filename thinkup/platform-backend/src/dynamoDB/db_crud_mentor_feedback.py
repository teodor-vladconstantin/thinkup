class DB_CRUD_MENTOR_FEEDBACK:
  def __init__(self, feedbackTable):
    self.__feedbackTable = feedbackTable

  def getFeedback(self, idOfTheFeedback: str):
    """Get a mentor feedback from the database

    Args:
        idOfTheFeedback (str): id of the feedback to get

    Returns:
        JSON: JSON of the feedback
    """
    response = self.__feedbackTable.get_item(
      Key={
        'id': idOfTheFeedback
      }
    )
    try:
      return response["Item"]
    except KeyError:
      return {"ErrorMessage": "Feedback Does not Exist"}

  def addFeedback(self, feedbackObjJSON: dict):
    """Adds a feedback to the database

    Args:
        feedbackObjJSON (dict): JSON Encoded version of the feedback object

    Returns:
        _type_: response
    """
    response = self.__feedbackTable.put_item(
      Item=feedbackObjJSON
    )
    return response

  def deleteFeedback(self, idOfTheFeedback: str):
    """Deletes a feedback from the database

    Args:
        idOfTheFeedback (str): id of the feeedback to delete

    Returns:
        _type_: response
    """
    response = self.__feedbackTable.delete_item(
      Key={
        'id': idOfTheFeedback
      }
    )
    return response

  
  def editFeedback(self, idOfTheFeedback: str,  editedFeedbackJSON: dict):
    """
    Edits a feedback from the database
    """

    response = self.__feedbackTable.update_item(
      Key={
        'id': idOfTheFeedback
      },
      UpdateExpression="SET #feedback_txt = :txt, #update_date = :date", 
      ExpressionAttributeNames={
        '#feedback_txt': 'feedback_txt',
        '#update_date': 'date'
      },
      ExpressionAttributeValues={
          ':txt': editedFeedbackJSON['feedback_txt'],
          ':date': editedFeedbackJSON['date']
      },
      ReturnValues="UPDATED_NEW"
    )
    return response
