import asyncio
from replit.database import AsyncDatabase
from replit import db
from aiohttp import ClientResponseError
import logging
repldb=AsyncDatabase(db.db_url)

class dberror(Exception):
	pass

sem = asyncio.Semaphore(3)
errorsem=asyncio.Semaphore(1)

async def tryrun(coro,*args,**kargs):
	async with sem:
		try:
			return await coro(*args,**kargs)
		except ClientResponseError:
			pass
		async with errorsem:
			retrynum=0
			waittime=1
			while True:
				retrynum=retrynum+1
				try:
					return await coro(*args,**kargs)
				except ClientResponseError as e:
					try:
						raise dberror(f'failed to run {repr(coro)} with arguments {str(args)}, {str(kargs)} in try number {retrynum}') from e
					except dberror as e2:
						if retrynum<10:
							logging.exception(e2)
							await asyncio.sleep(waittime)
							waittime*=2
						else:
							raise e2


async def tryset(key:str,val:str):
	if val==None:
		try:
			await repldb.delete(key)
		except KeyError:
			pass
	else:
		await repldb.set_raw(key,val)
	return None

async def change(key:str,val:str):
	return await tryrun(tryset,key,val)

async def tryget(key:str):
	try:
		return await repldb.get_raw(key)
	except KeyError:
		return None

async def get(key:str):
	return await tryrun(tryget,key)

async def have(key:str):
	return (await get(key)) is not None