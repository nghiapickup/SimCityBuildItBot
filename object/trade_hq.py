from object import button
from object.button import BntFactory
from object.object import BasicObject


class TradeHq(BasicObject):
    def __init__(self):
        super().__init__('trade_hq')
        self.n_sample = 1
        self.location = self.object_location.parse_location('trade_hq', 'location')
        self.bnt_refresh = BntFactory.make(button.BNT_TRADE_HQ_REFRESH)
