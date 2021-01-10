import discord
from discord.ext import commands
import os
import sqlite3

intents = discord.Intents.default()
intents.members = True

db = sqlite3.connect('main.sqlite')
c = db.cursor()

bot = commands.Bot(command_prefix="+", intents=intents)

@bot.event
async def on_ready():
    print("Hello World!")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="-help | v0.5"))

@bot.event
async def on_member_join(member: discord.Member):
    c.execute(f'SELECT channel_id, message, role FROM welcome WHERE guild_id = {member.guild.id}')
    result = c.fetchone()
    if result is None:
        return
    if result is not None:
        if result[2] is None:
            return
        elif result[2] is not None:
            role = discord.utils.get(member.guild.roles, name=f'{result[2]}')
            await member.add_roles(role)
        if result[1] is None:
            return
        elif result[1] is not None:
            username = member.name
            memberCount = len(list(member.guild.members))
            mention = member.mention
            guildName = member.guild
            canal = bot.get_channel(id=int(result[0]))
            await canal.send(str(result[1]).format(mention=mention, username=username, memberCount=memberCount, guildName=guildName))

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'`{extension}` fue cargado satisfactoriamente')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f'`{extension}` fue removido satisfactoriamente')

@bot.command()
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'`{extension}` fue recargado satisfactoriamente')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run('TOKEN')
