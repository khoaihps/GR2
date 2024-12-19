from telethon import TelegramClient
from telethon.events import NewMessage
from message_classifier import classify_message
import os


API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")


async def fetch_channel_messages(client, channel_username, topic):
    channel = await client.get_entity(channel_username)

    @client.on(NewMessage(chats=channel))
    async def new_message_handler(event):
        message = event.message.message
        print(f"New message in {channel_username}: {message}")

        classification_result = classify_message(message)
        if classification_result:
            key, value = classification_result
            print(f"Message classified as: {key}")
            print(f"Extracted value: {value}")

            if key:
                await topic.send(key=key, value=value)
                print(f"Message sent to Kafka topic: {value}")

    print(f"Listening to channel: {channel_username}")
    await client.run_until_disconnected()

async def create_telegram_client(channel_username):
    client = TelegramClient(f"session_{channel_username}", API_ID, API_HASH)
    await client.start()
    return client
