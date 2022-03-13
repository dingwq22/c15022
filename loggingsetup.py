import logging
from discordbot import client
from discord.ext import commands
import asyncio
import utils
from setup import logging_channel


async def sendservererror(log_entry):
	try:
		file=await utils.filefromstring(log_entry,'exception.txt')
		channel=client.get_channel(logging_channel)
		await channel.send('**Server Error**',file=file)
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
	if isinstance(error, commands.CommandNotFound):
		return  # Return because we don't want to show an error for every command not found
	elif isinstance(error, commands.CommandOnCooldown):
		message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
	elif isinstance(error, commands.MissingPermissions):
		message = "You are missing the required permissions to run this command!"
	elif isinstance(error, commands.UserInputError):
		message = "Something about your input was wrong, please check your input and try again!"
	else:
		message = "Oh no! Something went wrong while running the command!"
	await ctx.send(message, delete_after=5)
	await ctx.message.delete(delay=5)


havesetup=False
def setup():
	global havesetup
	if havesetup==False:
		client.add_cog(cogerrorhandler(client))
		havesetup=True
		dh = discordhandler()
		dh.setLevel(logging.WARNING)
		logging.getLogger().addHandler(dh)
		discorddlogger = logging.getLogger('discord')
		discorddlogger.setLevel(logging.WARNING)
		discorddlogger.addHandler(dh)
