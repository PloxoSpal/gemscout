from enum import Enum

class QuantityType(str, Enum):
    SINGLE_STONE = 'single_stone'
    PAIR = 'pair'
    LAYOUT = 'layout'
    PARCEL = 'parcel'

class RequestType(str, Enum):
    BUY = 'buy'
    SELL = 'sell'

class OfferType(str, Enum):
    BUY = "buy"
    SELL = "sell"

class RequestDuration(str, Enum):
    HOURLY = 'hourly'
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'