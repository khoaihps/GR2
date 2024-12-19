import asyncio
from telegram_fetcher import create_telegram_client, fetch_channel_messages
import faust

app = faust.App(
    'telegram-to-kafka',
    broker='kafka.default.svc.cluster.local:9092',
    # broker='kafka:9092',
)
topic = app.topic('telegram-messages')

async def main():
    channel = 'TestOrderB'

    client = await create_telegram_client(channel)
    await fetch_channel_messages(client, channel, topic)

if __name__ == '__main__':
    asyncio.run(main())