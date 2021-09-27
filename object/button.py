from object.object import BasicObject

# Button type
BNT_EMPTY = 100
BNT_TRADE_NEW = 101
BNT_COLLECT = 102
BNT_AD_WATCH = 103
BNT_AD_CLOSE = 104
BNT_AD_REWARD = 105
BNT_NO_THANKS = 106
BNT_TRADE_PLUS = 107
BNT_TRADE_DONE = 108
BNT_CLOSE_BLUE = 109
BNT_TRADE_PUT = 110
BNT_AD_REWARD_COLLECTED = 111
BNT_RIGHT = 112

BNT_TYPE = {
    'bnt_empty': BNT_EMPTY,
    'bnt_trade_new': BNT_TRADE_NEW,
    'bnt_collect': BNT_COLLECT,
    'bnt_ad_watch': BNT_AD_WATCH,
    'bnt_ad_close': BNT_AD_CLOSE,
    'bnt_ad_reward': BNT_AD_REWARD,
    'bnt_no_thanks': BNT_NO_THANKS,
    'bnt_trade_plus': BNT_TRADE_PLUS,
    'bnt_trade_done': BNT_TRADE_DONE,
    'bnt_close_blue': BNT_CLOSE_BLUE,
    'bnt_trade_put': BNT_TRADE_PUT,
    'bnt_ad_reward_collected': BNT_AD_REWARD_COLLECTED,
    'bnt_right': BNT_RIGHT,
}


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


class BntRight(BasicObject):
    def __init__(self):
        super().__init__('bnt_right')
        self.n_sample = 2
        self.threshold = 0.7


class BntFactory(BasicObject):
    bnt_map = {
        BNT_EMPTY: BntEmpty,
        BNT_TRADE_NEW: BntTradeNew,
        BNT_COLLECT: BntCollect,
        BNT_AD_WATCH: BntAdWatch,
        BNT_AD_CLOSE: BntAdClose,
        BNT_AD_REWARD: BntAdReward,
        BNT_NO_THANKS: BntNoThanks,
        BNT_TRADE_PLUS: BntTradePlus,
        BNT_TRADE_DONE: BntTradeDone,
        BNT_CLOSE_BLUE: BntCloseBlue,
        BNT_TRADE_PUT: BntTradePut,
        BNT_AD_REWARD_COLLECTED: BntAdRewardCollected,
        BNT_RIGHT: BntRight
    }

    @staticmethod
    def get(bnt_id):
        return BntFactory.bnt_map[bnt_id]()