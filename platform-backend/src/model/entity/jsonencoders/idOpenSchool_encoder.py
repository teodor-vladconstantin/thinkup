class IdOpenSchoolEncoder():
  def toJson(id: str, total_views: int, search_term: str, extension: str):
    newItem = {
      'id': id,
      'total_views': total_views,
      'search_term': search_term,
      'extension': extension,
    }
    return newItem