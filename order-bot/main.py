import faust
import sys
from discord_hook import send_to_discord
from db import save_signal_to_db

app = faust.App(
    'telegram-processor',
    broker='kafka.default.svc.cluster.local:9092',
    # broker='kafka:9092',
)
topic = app.topic('telegram-messages')

DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1289635123746050111/JDQmixla0xCFf7uyII_evddKo_aQjvwnBZLZbnv88pyvQTxiFNh5R863HDraU0vChEXM'

@app.agent(topic)
async def process_telegram_messages(messages):
    async for raw_message in messages:
        print(f"Raw message: {raw_message}")
        message = dict(raw_message)
        if 'news' in message:
            news_content = message['news']
            if news_content:
                await send_to_discord(news_content)
        else:
            order_result = {
                'type': 'LONG',
                'symbol': message['symbol'],
                'entry': message['entry'],
                'stop_loss': message['stop_loss'],
                'take_profit': message['take_profit'],
                'open_price': message['entry'],
                'close_price': message['take_profit'],
                'timestamp': message['timestamp'],
            }
            order_result['realized_pnl'] = (order_result['close_price']/order_result['open_price']-1)*10*20
            await save_signal_to_db(order_result)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.argv.extend(["worker", "-l", "info"])
    app.main()
