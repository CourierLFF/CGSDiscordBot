import asyncio
import os
import threading
import discord
import datetime
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
        gameStatus = 'Playing'
        accentColor = discord.Color.green()
        if data['game_state'] == 'Playing':
            gameStatus = 'Game Started'
            accentColor = discord.Color.blue()
        elif data['game_state'] == 'Completed':
            gameStatus = 'Game Finished'
            accentColor = discord.Color.green()
        elif data['game_state'] == 'Dropped':
            gameStatus = 'Game Dropped'
            accentColor = discord.Color.red()
        

        if channel:
            embed = discord.Embed(
                title=gameStatus,
                color=accentColor,
                timestamp=datetime.datetime.utcnow()
            )

            embed.set_author(name=data['name'], icon_url=data['cover_art'])
            embed.set_thumbnail(url=data['cover_art'])
            if data['game_state'] == 'Completed':
                embed.add_field(
                    name='Rating',
                    value=f"{data['user_rating']} / 100",
                )

            channel.send(embed=embed)
            asyncio.run_coroutine_threadsafe(
                channel.send(embed=embed),
                client.loop
            )
    
    receiver_thread = threading.Thread(
        target=start_receiver,
        args=(receiver_callback,),
        daemon=True
    )

    receiver_thread.start()

client.run(token)