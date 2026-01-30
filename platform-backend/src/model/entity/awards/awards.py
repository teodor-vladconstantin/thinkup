from model.entity.awards.award import Award


class Awards:
    def __init__(self, awards: list):
        self.__awards = awards

    def add_award(self, award: Award):
        self.__awards.append(award)

    def delete_award(self, awardId: str):
        for award in self.__awards:
            if award.get_id() == awardId:
                self.__awards.remove(award)

    def get_awards(self):
        return self.__awards
