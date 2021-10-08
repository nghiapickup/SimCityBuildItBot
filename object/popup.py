from object.object import BasicObject

# Template id
# POPUP_AD = 1
# POPUP_HEALTH = 2
# POPUP_SLEEP = 3
# POPUP_FIRE = 4
# POPUP_ROAD = 5
# POPUP_BOOK = 6
# POPUP_HOUSE = 7
# POPUP_GREEN = 8
# POPUP_SEA = 9
# POPUP_GOV = 10
# POPUP_PARK = 11
# POPUP_POLICE = 12
# POPUP_COFFEE = 13
# POPUP_RELAX = 14
# POPUP_SIMOLEON1 = 15
# POPUP_SIMOLEON2 = 16
#
# POPUP_TEMPLATE_NAME = {
#     POPUP_AD: 'POPUP_AD',
#     POPUP_HEALTH: 'POPUP_HEALTH',
#     POPUP_SLEEP: 'POPUP_SLEEP',
#     POPUP_FIRE: 'POPUP_FIRE',
#     POPUP_ROAD: 'POPUP_ROAD',
#     POPUP_BOOK: 'POPUP_BOOK',
#     POPUP_HOUSE: 'POPUP_HOUSE',
#     POPUP_GREEN: 'POPUP_GREEN',
#     POPUP_SEA: 'POPUP_SEA',
#     POPUP_GOV: 'POPUP_GOV',
#     POPUP_PARK: 'POPUP_PARK',
#     POPUP_POLICE: 'POPUP_POLICE',
#     POPUP_COFFEE: 'POPUP_COFFEE',
#     POPUP_RELAX: 'POPUP_RELAX',
#     POPUP_SIMOLEON1: 'POPUP_SIMOLEON1',
#     POPUP_SIMOLEON2: 'POPUP_SIMOLEON2'
# }


class OpinionPopup(BasicObject):
    def __init__(self):
        super().__init__("opinion_popup")
        self.n_sample = 14
        self.threshold = 0.7


class AdPopup(BasicObject):
    def __init__(self):
        super().__init__("ad_popup")
        self.n_sample = 1
        self.threshold = 0.7


class SimoleonPopup(BasicObject):
    def __init__(self):
        super().__init__("simoleon_popup")
        self.n_sample = 2
        self.threshold = 0.7