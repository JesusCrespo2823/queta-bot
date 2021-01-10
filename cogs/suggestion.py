import discord
from discord.ext import commands
import sqlite3

db = sqlite3.connect('./main.sqlite')
c = db.cursor()
c.execute('''
	CREATE TABLE IF NOT EXISTS suggestion(
		guild_id TEXT,
		channel_id TEXT
	)
''')

class Suggest(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.group(invoke_without_command=True)
	async def suggestion(self, ctx):
		mbed = discord.Embed(title="Configurar sistema de sugerencias", color=0x008cff)
		mbed.add_field(name=":mailbox_closed: Para colocar un canal", value="`suggestion channel <channel>`")
		await ctx.send(embed=mbed)

	@suggestion.command()
	async def channel(self, ctx, channel: discord.TextChannel):
		c.execute(f'SELECT channel_id FROM suggestion WHERE guild_id = {ctx.guild.id}')
		result = c.fetchone()
		if result is None:
			sql = ('INSERT INTO suggestion(guild_id, channel_id) VALUES(?, ?)')
			val = (ctx.guild.id, channel.id)
		if result is not None:
			sql = ('UPDATE suggestion SET channel_id = ? WHERE guild_id = ?')
			val = (channel.id, ctx.guild.id)
		c.execute(sql, val)
		db.commit()
		await ctx.send(f'El canal de sugerencias es ahora {channel.mention}')

	@commands.command()
	async def suggest(self, ctx, *args):
		s = " ".join(args)
		c.execute(f'SELECT channel_id FROM suggestion WHERE guild_id = {ctx.guild.id}')
		result = c.fetchone()
		if result is None:
			await ctx.send(s)
		elif result is not None:
			canal = self.bot.get_channel(id=int(result[0]))
			mbed = discord.Embed(title='Nueva sugerencia!', description=s, color=0x008cff)
			mbed.set_footer(text=f"Enviada por {ctx.author}")
			m = await canal.send(embed=mbed)
			await m.add_reaction("👍")
			await m.add_reaction("👎")

def setup(bot):
	bot.add_cog(Suggest(bot))