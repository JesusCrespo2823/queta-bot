import discord
from discord.ext import commands
from urllib import parse, request
import re

class Search(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def search(self, ctx, *, search):
		r = "https://google.com/search?q="+parse.quote(search)
		mbed = discord.Embed(title=search, url=r, color=0x008cff)
		mbed.set_author(name="🔍 Resultados de la busqueda")
		mbed.set_footer(text=f"Pedido por {ctx.author}")
		await ctx.send(embed=mbed)


def setup(bot):
	bot.add_cog(Search(bot))