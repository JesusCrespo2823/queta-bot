import discord
from discord.ext import commands
import sqlite3

db = sqlite3.connect('./main.sqlite')
c = db.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS welcome(
        guild_id TEXT,
        channel_id TEXT,
        message TEXT,
        role TEXT
    ) 
''')

class Configuration(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.group(invoke_without_command = True)
	async def welcome(self, ctx):
		mbed = discord.Embed(title="Welcome Commands", color=0x008cff)
		mbed.add_field(name="📪 Set A Channel", value="`welcome channel <channel>`")
		mbed.add_field(name="📄 Set a Message", value="`welcome message <message>`")
		mbed.add_field(name="Variables de mensaje", value="`{username}` = Nombre del usuario \n `{mention}` = Mencion al usuario \n `{memberCount}` = Conteo de los miembros del server \n `{guildName}` = Nombre del server \n `{discriminator}` = Muestra el tag del usuario", inline=False)
		await ctx.send(embed=mbed)

	@welcome.command()
	@commands.has_permissions(manage_channels=True)
	async def channel(self, ctx, channel: discord.TextChannel):
		c.execute(f'SELECT channel_id FROM welcome WHERE guild_id = {ctx.guild.id}')
		result = c.fetchone()
		if result is None:
			sql = ('INSERT INTO welcome(guild_id, channel_id) VALUES(?, ?)')
			val = (ctx.guild.id, channel.id)
		if result is not None:
			sql = ('UPDATE welcome SET channel_id = ? WHERE guild_id = ?')
			val = (channel.id, ctx.guild.id)
		c.execute(sql, val)
		db.commit()
		await ctx.send(f':mailbox_with_mail: El canal de bienvenidas es ahora {channel.mention}')

	@channel.error
	async def error_channel(self, ctx, error):
		if isinstance(error, commands.MissingPermissions):
			await ctx.send('No tienes permisos para usar este comando')

	@welcome.command()
	@commands.has_permissions(manage_channels=True)
	async def message(self, ctx, *args):
		msg = " ".join(args)
		c.execute(f'SELECT message FROM welcome WHERE guild_id = {ctx.guild.id}')
		result = c.fetchone()
		if result is None:
			sql = ('INSERT INTO welcome(guild_id, message) VALUES(?, ?)')
			val = (ctx.guild.id, msg)
		if result is not None:
			sql = ('UPDATE welcome SET message = ? WHERE guild_id = ?')
			val = (msg, ctx.guild.id)
		c.execute(sql, val)
		db.commit()
		mbed = discord.Embed(title="✅ El mensaje de bienvenida es ahora: ", description=f"`{msg}`", color=0x008cff)
		await ctx.send(embed=mbed)

	@welcome.command()
	@commands.has_permissions(manage_roles=True)
	async def role(self, ctx, role: discord.Role):
		c.execute(f'SELECT role FROM welcome WHERE guild_id = {ctx.guild.id}')
		result = c.fetchone()
		if result is None:
			sql = ('INSERT INTO welcome(role, guild_id) VALUES(?, ?)')
			val = (role.name, ctx.guild.id)
		elif result is not None:
			sql = ('UPDATE welcome SET role = ? WHERE guild_id = ?')
			val = (role.name, ctx.guild.id)
		c.execute(sql, val)
		db.commit()
		await ctx.send(f'✅ Ahora a todos los nuevos miembros que se unan se les asignara el rol {role.mention}')

	@welcome.command()
	@commands.has_permissions(manage_channels=True)
	async def off(self, ctx):
		mbed = discord.Embed(title='Estas seguro?', description="Este proceso borrara el canal de bienvenidas, tu mensaje actualmente establecido y el autoroles, asi que si quieres volver a activarlo tendras que establecerlos de vuelta \n\n ✅ Y = Si \n\n ❌ N = No")
		def check(m):
			return m.author.id == ctx.author.id
		await ctx.send(embed=mbed)
		d = await self.bot.wait_for('message', check=check)
		st = d.content.lower()	
		if st == "y":
			c.execute(f'DELETE FROM welcome WHERE guild_id = {ctx.guild.id}')
			await ctx.send('Bienvenida desactivada')
		elif st == "n":
			mbed = discord.Embed(description="Proceso cancelado")
			await ctx.send(embed=mbed)
		else:
			await ctx.send('Opcion no valida, trate de nuevo')

	@welcome.command()
	async def test(self, ctx, member: discord.Member):
		c.execute(f'SELECT channel_id, message FROM welcome WHERE guild_id = {ctx.guild.id}')
		result = c.fetchone()
		username = member.name
		memberCount = len(list(member.guild.members))
		discriminator = f'#{member.discriminator}'
		mention = member.mention
		guildName = member.guild
		canal = self.bot.get_channel(id=int(result[0]))
		await canal.send(str(result[1]).format(mention=mention, username=username, memberCount=memberCount, guildName=guildName, discriminator=discriminator))

def setup(bot):
	bot.add_cog(Configuration(bot))