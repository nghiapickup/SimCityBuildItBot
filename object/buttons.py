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