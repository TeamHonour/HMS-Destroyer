# Imports.
import os

import disnake
from disnake.ext import commands
from decouple import UndefinedValueError, config
import aiocron

try:
    discord_token = config('DISCORD_BOT_TOKEN', cast=str)
    guild_id = config('GUILD_ID', cast=int)
    channel_id = config('CHANNEL_ID', cast=int)
    timeout = config('TIMEOUT', cast=int)
    public_shame = config('PUBLIC_SHAME', cast=bool)
except UndefinedValueError:
    print("Envronments variables were left undefined.")
    exit(1)

intents = disnake.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix=">>>", intents=intents)

@bot.event
async def on_ready():
    os.system('clear')
    print("Ready for attack.")

# Run the cronjob every 1 minute.
@aiocron.crontab('*/1 * * * *')
async def cronjob():
    guild = bot.get_guild(guild_id)
    channel = guild.get_channel(channel_id)
    for member in guild.members:
        if member.activity != None:
            if member.activity.name.lower() == "sea of thieves":
                if member.current_timeout == None:
                    # Timeout for <x> seconds
                    await member.timeout(duration=timeout)
                    if public_shame:
                        await channel.send(f"{member.name} has been shadowed by the Navy.")
                    else:
                        await member.send("You have been shadowed by the Navy.")

bot.run(discord_token)