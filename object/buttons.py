from object.objects import BasicObject


class BntEmpty(BasicObject):
    def __init__(self):
        super().__init__("bnt_empty")
        self.n_sample = 2
        self.threshold=0.9


class BntTradeNew(BasicObject):
    def __init__(self):
        super().__init__("bnt_trade_new")
        self.n_sample = 1
        self.threshold = 0.9


class BntTradePlus(BasicObject):
    def __init__(self):
        super().__init__('bnt_trade_plus')
        self.n_sample = 1
        self.threshold = 0.9


class BntTradeDone(BasicObject):
    def __init__(self):
        super().__init__('bnt_trade_done')
        self.n_sample = 1
        self.threshold = 0.9


class BntTradePut(BasicObject):
    def __init__(self):
        super().__init__('bnt_trade_put')
        self.n_sample = 1
        self.threshold = 0.9


class BntCollect(BasicObject):
    def __init__(self):
        super().__init__("bnt_collect")
        self.n_sample = 1
        self.threshold = 0.9


class BntAdWatch(BasicObject):
    def __init__(self):
        super().__init__('bnt_ad_watch')
        self.n_sample = 1
        self.threshold = 0.9


class BntAdClose(BasicObject):
    def __init__(self):
        super().__init__('bnt_ad_close')
        self.n_sample = 2
        self.threshold = 0.9


class BntAdReward(BasicObject):
    def __init__(self):
        super().__init__('bnt_ad_reward')
        self.n_sample = 2
        self.threshold = 0.8


class BntAdRewardCollected(BasicObject):
    def __init__(self):
        super().__init__('bnt_ad_reward_collected')
        self.n_sample = 1
        self.threshold = 0.8


class BntNoThanks(BasicObject):
    def __init__(self):
        super().__init__('bnt_no_thanks')
        self.n_sample = 1
        self.threshold = 0.9


class BntCloseBlue(BasicObject):
    def __init__(self):
        super().__init__('bnt_close_blue')
        self.n_sample = 1
        self.threshold = 0.9
