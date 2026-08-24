class Permissions:
    def __init__(self, perms: dict):
        self.__perms = perms

    def get_perm(self):
        return self.__perms

    def check_perm(self, perm):
        return self.__perms.get(perm)
