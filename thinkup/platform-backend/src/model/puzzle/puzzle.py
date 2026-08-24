class Puzzle:
  def __init__(self, id, acquired_pieces_ids: set, missing_pieces_ids: set, total_pieces_ids: set):
    self.__id = id
    self.__acquired_pieces_ids = acquired_pieces_ids
    self.__missing_pieces_ids = missing_pieces_ids
    self.__total_pieces_ids = total_pieces_ids

  def get_id(self):
    return self.__id
  
  def get_acquired_pieces_ids(self):
    return self.__acquired_pieces_ids
  
  def get_missing_pieces_ids(self):
    return self.__missing_pieces_ids
  
  def get_total_pieces_ids(self):
    return self.__total_pieces_ids

  def acquire_piece(self, piece_id):
    try:
      self.__acquired_pieces_ids.add(piece_id)
      self.__missing_pieces_ids.remove(piece_id)
      return None
    except KeyError:
      return "Piece already acquired"

  

    