import discord
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions,  CheckFailure, check
from discord import PermissionOverwrite
import os



intents = discord.Intents.all()
client = commands.Bot(command_prefix = '',intents=intents) #put your own prefix here


@client.event
async def on_ready():
	print("bot online") #will print "bot online" in the console when the bot is online

    
@client.command()
async def ping(ctx):
	await ctx.send("pong!") #simple command so that when you type "!ping" the bot will respond with "pong!"

@client.command()
async def channelid(ctx):
	await ctx.send(ctx.message.channel.id)

@client.command()
async def categoryid(ctx):
	await ctx.send(ctx.message.channel.category_id)


from replit import db

try:
	privatechannels=db["privatechannels"]
except:
	privatechannels={}

@client.event
async def on_member_join(member):
	channel = client.get_channel(950555429413486682)
	await channel.send(f'{member.name} has joined the server')

	category = client.get_channel(950562991793901628)
	perms={
		member.guild.default_role: PermissionOverwrite(read_messages=False)
	}
	channel = await category.create_text_channel(member.name, overwrites=perms)

	await channel.set_permissions(member, read_messages=True, send_messages=True)

	privatechannels[member.id]=channel.id
	db["privatechannels"]=privatechannels
  


@client.command()
async def invite(ctx, member: discord.Member):
	channel_id = db["privatechannels"][ctx.author]
	channel = client.get_channel(950555429413486682)
	await channel.send(f'{ctx.author} send an invite')
	await channel.send(f'{member.name} has joined the channel')


@client.command()
async def simulatejoin(ctx, member : discord.Member):
	await on_member_join(member)
  
@client.command()
async def testexception(ctx):
	return 1/0



async def runbot():
	await client.start(os.getenv('TOKEN'))