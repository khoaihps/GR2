import faust
import requests
import sys
from model import Ticker
from datetime import datetime

BINANCE_API_URL = "https://api.binance.com/api/v3/ticker/price"
SYMBOLS = ["BTCUSDT", "OPUSDT", "NEARUSDT", "PEPEUSDT", "XRPUSDT", "EIGENUSDT"]

app = faust.App(
    'binance-price-stream',
    broker='kafka.default.svc.cluster.local',
    # broker='kafka:9092',
)

tick_topic = app.topic('ticker', value_type=Ticker)

@app.timer(interval=1)
async def fetch_price_data():
    try:
        response = requests.get(BINANCE_API_URL, params={"symbols": str(SYMBOLS).replace("'", '"').replace(', ',',')})
        response.raise_for_status()
        data = response.json()

        for item in data:
            ticker = Ticker(
                symbol=item['symbol'],
                price=float(item['price']),
                timestamp=int(datetime.now().timestamp()),
            )
            await tick_topic.send(key=item['symbol'], value=ticker)
            print(f"Sent to Kafka: {ticker}")

    except Exception as e:
        print(f"Error fetching data: {e}")


@app.agent(tick_topic)
async def process_prices(prices):
    async for price in prices:
        print(f"Received from Kafka: {price.symbol} | Price: {price.price}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.argv.extend(["worker", "-l", "info"])
    app.main()