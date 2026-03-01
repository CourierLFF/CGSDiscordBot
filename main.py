import asyncio
import os
import threading
import discord
from dotenv import load_dotenv
from receiver import start_receiver

load_dotenv()

token = os.getenv('TOKEN')
channel_id = int(os.getenv('CHANNEL_ID'))

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    def receiver_callback(data):
        channel = client.get_channel(channel_id)
        if channel:
            asyncio.run_coroutine_threadsafe(
                channel.send(f'Received data: {data['message']}'),
                client.loop
            )
    
    receiver_thread = threading.Thread(
        target=start_receiver,
        args=(receiver_callback,),
        daemon=True
    )

    receiver_thread.start()

client.run(token)