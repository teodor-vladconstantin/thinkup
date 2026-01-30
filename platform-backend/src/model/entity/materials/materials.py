from model.entity.materials.material import Material

class Materials:
  def __init__(self, materials: list):
    self.__materials = materials

  def get_materials(self):
    return self.__materials

  def add_material(self, new_material: Material):
    self.__materials.append(new_material)

  def get_material(self, id: str):
    for material in self.__materials:
      if material.get_id() == id:
          return material
    return None

  def delete_material(self, id: str):
    for material in self.__materials:
      if material.get_id() == id:
          self.__materials.remove(material)

  def update_material(self, idOfMaterial: str, new_material: Material):
    for material in self.__materials:
      if material.get_id() == idOfMaterial:
          material = new_material
          return