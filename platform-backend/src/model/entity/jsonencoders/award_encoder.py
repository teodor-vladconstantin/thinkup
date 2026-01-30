from ..awards.award import Award


class AwardEncoder():
    def toJson(award):
        if isinstance(award, Award):
            newItem={
                'id': award.get_id(),
                'name': award.get_name(),
                'userId': award.get_userId(),
                'description': award.get_description(),
                'imageId': award.get_imageId()
            }
            return newItem

        return None

"""
JSON Format:
{
    "name": "1 days working streak",
    "description": "Enter the platform for 1 day in a row to earn this award",
    "userId": "115894574668091398078",    
    "imageId": "asd123"
}
"""