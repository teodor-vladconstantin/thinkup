from ..project import Project


class ProjectEncoder():
  def toJSON(o):
    if isinstance(o, Project):
      Item = {
        'id': o.get_id(),
        'name': o.get_name(),
        'createdBy': o.get_createdBy(),
        'adminList': list(o.get_adminList()),
        'searchTerm': o.get_searchTerm(),
        'description': o.get_description(),
        'creationDate': o.get_creationDate(),
        'thumbnail': o.get_thumbnail(),
        'thumbnail_extension': o.get_thumbnail_extension(),
        'areaOfImplementation': o.get_areOfImplementation(),
        'goals': o.get_goals().get_goals(),
        'materials': o.get_materials().get_materials(),
        'settings': o.get_settings(),
        'projectReviews': {
          'total_reviews': o.get_projectReviews().get_total_reviews(),
          'average_rating': o.get_projectReviews().get_average_rating(),
          'reviews': o.get_projectReviews().get_reviews()
        },
        'mentor_feedback': o.get_mentor_feedback(),
      }
      return Item
    return None


# USE : ProjectEncoder().toJSON(proj)

"""
JSON Format :

{
    "id": "testProj1",
    "name": "ThinkUp Project #1",
    "created_by": "Crisan Alexandru",
    "adminList": ["user123", "user4", "Crisan Alexandru"],
    "description": "Amazing project built by 2 students",
    "creation_date": "13/2/2022",
    "thumbnail": -,
    "area_of_implementation": "Environment",
    "goals": ["id#1", "id#3"],
    "materials": ["id#1", "id#2"]
}
"""
