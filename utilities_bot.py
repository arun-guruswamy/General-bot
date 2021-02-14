from discord.ext import commands, tasks
import discord
import datetime

client = commands.Bot(command_prefix = "/")

client.ANNOUNCEMENTS = None

@client.event
async def on_ready():
    print('Bot is online')

@tasks.loop(hours=24)
async def game_poll():
    d = datetime.datetime.now()
    day = d.strftime("%a")
    if day == "Thu":
        await client.ANNOUNCEMENTS.send("Alright @everyone! game night this saturday at 7 pm IST, let us know if you can make it!")
        await client.ANNOUNCEMENTS.send('/poll "Can you make it for game night" "Yes!" "Sadly no..." "Not sure yet"')
        await client.ANNOUNCEMENTS.purge(limit=1)
        
@client.command()
async def setup(ctx):
        client.ANNOUNCEMENTS = discord.utils.get(ctx.guild.channels, name="announcements")
        game_poll.start()

client.run('ODA3MDg0ODAyMjIxNjcwNDgw.YBy2Sw.WPQc9ZgAD3bPv1ZyBwoYtsbS8UY')