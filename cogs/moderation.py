import discord
from discord.ext import commands

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kick(self, ctx):
        await ctx.send('Kick Command')
    
    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason="No se especifico una razon"):
        mbed = discord.Embed(title=":hammer: Usuario Baneado", color=0x008cff)
        mbed.add_field(name="Usuario: ", value=member.mention)
        mbed.add_field(name="Razon: ", value=reason, inline=False)
        mbed.add_field(name="Moderador responsable: ", value=ctx.author)
        mbed.set_footer(text=f"Administracion de {ctx.guild}")
        await ctx.send(embed=mbed)
        await member.send(embed=mbed)
        await member.ban(reason=reason)
    
    @commands.command(aliases=['cls', 'purge'])
    async def clear(self, ctx, amount=100):
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)

    @commands.command()
    async def eval(self, ctx, *, command):
        res = eval(command)
        await ctx.send(res)

def setup(bot):
    bot.add_cog(Moderation(bot))
