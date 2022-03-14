import discord
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions,  CheckFailure, check
from discord import PermissionOverwrite
import os
from utils import format_exception, filefromstring
import typing
import json
import setup
import database as db


intents = discord.Intents.all()
client = commands.Bot(command_prefix = '',intents=intents) #put your own prefix here


async def predicate(ctx):
	return setup.permrole in [x.id for x in ctx.author.roles]
haveperm=commands.check(predicate)


@client.event
async def on_ready():
	print("bot online") #will print "bot online" in the console when the bot is online

@client.command()
async def ping(ctx):
	#simple command so that when you type "!ping" the bot will respond with "pong!"
	await ctx.send("pong!")

@client.command(name="helloworld")
async def ping2(ctx):
	#simple command so that when you type "!ping" the bot will respond with "pong!"
	await ctx.send("pong!")

@client.command()
@haveperm
async def gettutorial(ctx):
	f = open("tutorial.txt", "r")
	await client.get_channel(952607462534565968).send(f.read())

@client.event
async def on_message(message):
	await client.process_commands(message) 
	if message.content.lower().startswith("how are you") and not message.author.bot:
		await message.channel.send("Good!")

@client.command()
async def echo(ctx, text):
	await ctx.send('```'+text+'```')

@client.command()
async def channelid(ctx):
	await ctx.send(ctx.message.channel.id)

@client.command()
async def categoryid(ctx):
	await ctx.send(ctx.message.channel.category_id)

@client.command()
@haveperm
async def getdb(ctx):
	formatted=json.dumps(await db.getall(),indent=2)
	await ctx.send(file=await filefromstring(formatted, "db.txt"))
	
#https://stackoverflow.com/questions/44859165/async-exec-in-python
async def async_exec(code,ctx):
	global privatechannels
	try:
		exec(
			f'async def __aexecinternal(ctx): ' +
			''.join(f'\n {l}' for l in code.split('\n'))
		)
		# Get `__aexecinternal` from local variables, call it and return the result
		tmp=await locals()['__aexecinternal'](ctx)
	except Exception as e:
		return format_exception(e)
	return tmp
		
@client.command()
@haveperm
async def aexec(ctx, *, ipt):
	try:
		if ipt[:3]==ipt[-3:]=='```':
			ipt=ipt[3:-3]
		elif ipt[:1]==ipt[-1:]=='`':
			ipt=ipt[1:-1]
	except:
		pass
	ans=await async_exec(ipt, ctx)
	await ctx.send(file=await filefromstring(ans, "aexec.txt"))


privatechannels=None
@client.event
async def on_member_join(member):
	global privatechannels
	channel = client.get_channel(950555429413486682)
	await channel.send(f'{member.name} has joined the server')

	category = client.get_channel(950562991793901628)
	perms={
		member.guild.default_role: PermissionOverwrite(read_messages=False)
	}
	channel = await category.create_text_channel(member.name, overwrites=perms)

	await channel.set_permissions(member, read_messages=True, send_messages=True)

	# set "Student" role to member  
	if (not member.bot):
		role = "student"
		await member.add_roles(discord.utils.get(member.guild.roles, name=role))

		if privatechannels is None:
			privatechannels=await db.get("privatechannels")
		privatechannels[str(member.id)]=channel.id
		await db.set("privatechannels",privatechannels)
  

@client.command()
async def testname(ctx, member : typing.Union[discord.Member, discord.Role]):
	await ctx.send(repr(member))

	
@client.command()
async def invite(ctx, member : typing.Union[discord.User, discord.Role]):
	global privatechannels
	if privatechannels is None:
		privatechannels=await db.get("privatechannels")
	author_name = ctx.author.name
	# channel = discord.utils.get(ctx.guild.channels, name=author_name)
	channel = client.get_channel(privatechannels[str(ctx.author.id)])
	await channel.send(f'{author_name} invite {member.mention} to the channel')
	await channel.set_permissions(member, read_messages=True, send_messages=True)


@client.command()
async def kick(ctx, member : typing.Union[discord.User, discord.Role]):
	global privatechannels
	if privatechannels is None:
		privatechannels=await db.get("privatechannels")
	author_name = ctx.author.name
	# channel = discord.utils.get(ctx.guild.channels, name=author_name)
	channel = client.get_channel(privatechannels[str(ctx.author.id)])
	await channel.set_permissions(member, read_messages=False, send_messages=False)
	await ctx.send(f'User {member.mention} has been kicked')



@client.command()
async def simulatejoin(ctx, member : discord.Member):
	await on_member_join(member)
  
@client.command()
async def testexception(ctx):
	return 1/0

@client.command()
async def get_channel(ctx):
	channel_name = ctx.author.name
	channel = discord.utils.get(ctx.guild.channels, name=channel_name)
	print(channel.id)

@client.command()
async def get_roles(ctx, member : discord.Member):
    await ctx.send(f'roles {member.roles}')

@client.command()
async def set_roles(ctx, member : typing.Union[discord.Member, discord.User]):
	# set "Student" role to member  
	role = "student"
	await member.add_roles(discord.utils.get(member.guild.roles, name=role))

@client.command()
async def isbot(ctx, member : typing.Union[discord.Member, discord.User]):
	print(member.bot)


async def runbot():
	await client.start(os.getenv('TOKEN'))
