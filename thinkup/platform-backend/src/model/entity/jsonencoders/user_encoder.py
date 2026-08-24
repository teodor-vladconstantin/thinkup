from model.entity.users.student import Student


class UserEncoder():
    def toJSON(o):
        if isinstance(o, Student):
            Item = {
                'id': o.get_id(),
                'name': o.get_name(),
                'search_term': o.get_search_term(),
                'profile_picture': o.get_profile_picture(),
                'profile_picture_extension': o.get_profile_picture_extension(),
                'cover_picture': o.get_cover_picture(),
                'cover_picture_extension': o.get_cover_picture_extension(),
                'email': o.get_email(),
                'description': o.get_description(),
                'settings': {
                    'language': o.get_settings().get_language(),
                    'notifications': o.get_settings().get_notifications(),
                    'theme': o.get_settings().get_theme()
                },
                'perms': o.get_perms().get_perm(),
                'activity': o.get_activity(),
                'puzzle': {
                    'id': o.get_puzzle().get_id(),
                    'acquired_pieces_ids': list(o.get_puzzle().get_acquired_pieces_ids()),
                    'missing_pieces_ids': list(o.get_puzzle().get_missing_pieces_ids()),
                    'total_pieces_ids': list(o.get_puzzle().get_total_pieces_ids())
                },
                'personal_objectives': o.get_personal_objectives(),
                'social_connections': o.get_social_connections(),
                'role': type(o).__name__,
                'fav_files': o.get_favFiles()
            }
            return Item
        return None



# USE : UserEncoder().toJSON(compt)

"""
JSON Format :

{
    "id": "1028",
    "name": "Crisan",
    "profile_picture": "idpriqi234"
    "email": "calex2005cj@gmail.com",
    "description": "coolest user alive",
    "settings": {
        "language": "ro",
        "notifications": true,
        "theme": false
    },
    "perms": {
        "canCreateProject": true,
        "canEditProject": true,
        "canDeleteProject": false
    },
    "projects": [
        "DemoProject1",
        "DemoProject2"
    ]
}

"""
