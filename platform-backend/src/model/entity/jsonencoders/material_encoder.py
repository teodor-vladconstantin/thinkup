from ..materials.material import Material

class MaterialEncoder:
  def toJSON(material):
    if isinstance(material, Material):
      Item = {
        'id': material.get_id(),
        'name': material.get_name(),
        'projectId': material.get_projectId(),
        'description': material.get_description(),
        'creationDate': material.get_creationDate(),
        'createdBy': material.get_createdBy(),
        'files': material.get_files()
      }
      return Item
    return None

"""
JSON Format:
{
    "id": "1010",
    "name": "Fisiere de inceput",
    "projectId": "",
    "description": "Fisierele de care aveti nevoie sa rulati programul",
    "creationDate": "13/4/2023",
    "createdBy": "userId#123",
    "files": [ "file#23", "file#4003", "file#1" ]
}
"""