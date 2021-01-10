import discord
from discord.ext import commands
import sqlite3
import random

db = sqlite3.connect('./main.sqlite')
c = db.cursor()
c.execute('''
        CREATE TABLE IF NOT EXISTS economy(
            guild_id TEXT,
            user_id TEXT,
            wallet INT,
            bank INT
        ) 
''')

class Economy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['bal'])
    async def balance(self, ctx):
        c.execute(f'SELECT wallet, bank FROM economy WHERE guild_id = {ctx.guild.id} AND user_id = {ctx.author.id}')
        result = c.fetchone()
        mbed = discord.Embed()
        if result is None:
            mbed.add_field(name='Wallet', value='0')
        elif result is not None:
            mbed.add_field(name='Wallet', value=result[0])
        if result[1] is None:
            mbed.add_field(name='Bank', value='0')
        elif result[1] is not None:
            mbed.add_field(name='Bank', value=result[1])
        await ctx.send(embed=mbed)
 
    @commands.command()
    async def work(self, ctx):
        c.execute(f'SELECT wallet FROM economy WHERE guild_id = {ctx.guild.id} AND user_id = {ctx.author.id}')
        result = c.fetchone()
        ganancias = random.randrange(550)
        if result is None:
            sql = ('INSERT INTO economy(guild_id, user_id, wallet) VALUES(?, ?, ?)')
            val = (ctx.guild.id, ctx.author.id, ganancias)
        elif result is not None:
            sql = ('UPDATE economy SET wallet = ? WHERE user_id = ? AND guild_id = ?')
            val = (int(result[0]) + ganancias, ctx.author.id, ctx.guild.id)
        c.execute(sql, val)
        db.commit()
        await ctx.send(f'Has ganado {ganancias}$')

def setup(bot):
    bot.add_cog(Economy(bot))
