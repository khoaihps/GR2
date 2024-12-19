from discord_webhook import DiscordWebhook
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1289635123746050111/JDQmixla0xCFf7uyII_evddKo_aQjvwnBZLZbnv88pyvQTxiFNh5R863HDraU0vChEXM'


async def send_to_discord(content):
    webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL, content=content)
    response = webhook.execute()
    if response.status_code == 200:
        print(f"Sent to Discord: {content}")
    else:
        print(f"Failed to send to Discord: {response.status_code}")