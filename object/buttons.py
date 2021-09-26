from object.objects import BasicObject


class BntEmpty(BasicObject):
    def __init__(self):
        super().__init__("bnt_empty")
        self.n_sample=6
        self.threshold=0.9


class BntTradeNew(BasicObject):
    def __init__(self):
        super().__init__("bnt_trade_new")


class BntCollect(BasicObject):
    def __init__(self):
        super().__init__("bnt_collect")


class BntAdWatch(BasicObject):
    def __init__(self):
        super().__init__('bnt_ad_watch')
        self.n_sample = 1


class BntAdClose(BasicObject):
    def __init__(self):
        super().__init__('bnt_ad_close')
        self.n_sample = 1


class BntAdReward(BasicObject):
    def __init__(self):
        super().__init__('bnt_ad_reward')
        self.n_sample = 1


class BntNoThanks(BasicObject):
    def __init__(self):
        super().__init__('bnt_no_thanks')
        self.n_sample = 1
