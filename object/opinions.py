from object.objects import BasicObject

OBLUE_AD = 1
OBLUE_HEALTH = 2
OBLUE_SLEEP = 3
OBLUE_FIRE = 4
OBLUE_ROAD = 5
OBLUE_BOOK = 6
OBLUE_HOUSE = 7
OBLUE_GREEN = 8
OBLUE_SEA = 9
OBLUE_GOV = 10
OBLUE_PARK = 11
OBLUE_POLICE = 12
OBLUE_COFFEE = 13
OBLUE_RELAX = 14

OSIMOLEON = 100

OPINION = {
    OBLUE_AD: 'OBLUE_AD',
    OBLUE_HEALTH: 'OBLUE_HEALTH',
    OBLUE_SLEEP: 'OBLUE_SLEEP',
    OBLUE_FIRE: 'OBLUE_FIRE',
    OBLUE_ROAD: 'OBLUE_ROAD',
    OBLUE_BOOK: 'OBLUE_BOOK',
    OBLUE_HOUSE: 'OBLUE_HOUSE',
    OBLUE_GREEN: 'OBLUE_GREEN',
    OBLUE_SEA: 'OBLUE_SEA',
    OBLUE_GOV: 'OBLUE_GOV',
    OBLUE_PARK: 'OBLUE_PARK',
    OBLUE_POLICE: 'OBLUE_POLICE',
    OBLUE_COFFEE: 'OBLUE_COFFEE',
    OBLUE_RELAX: 'OBLUE_RELAX',

    OSIMOLEON: 'OSIMOLEON'
}



class OpinionBlue(BasicObject):
    def __init__(self):
        super().__init__("opinion_blue")
        self.n_sample = 14
        self.threshold = 0.8


class OpinionSimoleon(BasicObject):
    def __init__(self):
        super().__init__("opinion_simoleon")
        self.n_sample = 2
        self.threshold = 0.9
