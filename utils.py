import io
import discord
import traceback

async def filefromstring(text,filename="file.txt"):
	f = io.StringIO(str(text))
	return discord.File(fp=f,filename=filename)



import datetime
import pytz

def timestringnow():
	return datetime.datetime.now(tz=pytz.timezone("US/Eastern"))
	
def loggingtimenow(*args):
	return timestringnow().timetuple()

def format_exception(error):
	return ''.join(traceback.format_exception(type(error), error, error.__traceback__))
