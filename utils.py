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
	return "".join(traceback.TracebackException.from_exception(error).format())



import base64
from passlib import pwd
from passlib.hash import sha512_crypt


def tocode(s):
	return base64.b16encode(s.encode()).decode()
def fromcode(s):
	return base64.b16decode(s.encode()).decode()

def generate_password():
	pwd.genword(entropy=512)
def hash_password(password):
	return tocode(sha512_crypt.hash(password,rounds=1000))
def verify_password(password,hash):
	return sha512_crypt.verify(password,fromcode(hash))