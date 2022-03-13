import io
import discord

async def filefromstring(text,filename="file.txt"):
	f = io.StringIO(str(text))
	return discord.File(fp=f,filename=filename)



import datetime
import pytz

def timestringnow():
	return datetime.datetime.now(tz=pytz.timezone("US/Eastern"))
	
def loggingtimenow(*args):
	return timestringnow().timetuple()