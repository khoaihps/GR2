import faust

class Ticker(faust.Record):
    symbol: str
    price: float
    timestamp: int