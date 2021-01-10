import discord
import time
import random
from discord.ext import commands

class Entertaiment(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['8ball'])
    async def _8ball(self, ctx, *args):
        await ctx.send('8ball Command')

    @commands.command()
    async def roll(self, ctx):
        m = await ctx.send(':game_die: Lanzando...')
        time.sleep(2)
        await m.edit(content=f':game_die: Haz sacado {random.randrange(7)}')

def setup(bot):
    bot.add_cog(Entertaiment(bot))
