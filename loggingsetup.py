import logging
from discordbot import client
from discord.ext import commands
import asyncio
import utils
from setup import logging_channel
import traceback
import sys

async def sendservererror(log_entry):
	try:
		file=await utils.filefromstring(log_entry,'exception.txt')
		channel=client.get_channel(logging_channel)
		await channel.send('**An Error Occured**',file=file)
	except Exception as e:
		print(e)
		print('due to the above exception, the following excpetion cannot be logged:')
		print(log_entry)

class discordhandler(logging.Handler):
	def emit(self, record):
		log_entry = self.format(record)
		try:
			asyncio.create_task(sendservererror(log_entry))
		except Exception as e:
			print(e)
			print('due to the above exception, the following excpetion cannot be logged:')
			print(log_entry)

#https://tutorial.vcokltfre.dev/tutorial/12-errors/
class cogerrorhandler(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	@commands.Cog.listener()
	async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
		"""A global error handler cog."""
		try:
			stacktrace=False
			if isinstance(error, commands.CommandNotFound):
				return	# Return because we don't want to show an error for every command not found
			elif isinstance(error, commands.CommandOnCooldown):
				message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
				stacktrace=True
			elif isinstance(error, commands.MissingPermissions):
				message = "You are missing the required permissions to run this command!"
				stacktrace=True
			elif isinstance(error, commands.UserInputError):
				message = "Something about your input was wrong, please check your input and try again!"
				stacktrace=True
			else:
				message = "Oh no! Something went wrong while running the command!"
				stacktrace=True
			if stacktrace:
				# In a production environment, you should never print the stacktrace!
				# you can send it to a private channel you specify in setup.py by simply reraising the error
				# it will then be caught and formatted in the logging.exception
				# raise error
				tracebackstring = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
				file=await utils.filefromstring(tracebackstring,'exception.txt')
				await ctx.send('there was an exception',file=file)
			else:
				await ctx.send(message, delete_after=5)
				await ctx.message.delete(delay=5)
		except Exception as e:
			logging.exception(e)

havesetup=False
def setup():
	global havesetup
	if havesetup==False:
		client.add_cog(cogerrorhandler(client))
		havesetup=True
		dh = discordhandler()
		dh.setLevel(logging.WARNING)
		logging.getLogger().addHandler(dh)
