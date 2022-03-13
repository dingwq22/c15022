# see documentation of replit.database here
# https://replit-py.readthedocs.io/en/latest/api.html
import setup


import asyncio
import logging

if setup.database=="replit":
	from replit.database import AsyncDatabase
	from replit import db
	from aiohttp import ClientResponseError
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
	
	
	async def tryset(key:str,val):
		if val==None:
			try:
				await repldb.delete(key)
			except KeyError:
				pass
		else:
			await repldb.set(key,val)
		return None
	
	async def set(key:str,val):
		return await tryrun(tryset,key,val)
	
	async def tryget(key:str):
		try:
			return await repldb.get(key)
		except KeyError:
			return None
	
	async def get(key:str):
		return await tryrun(tryget,key)
	
	async def have(key:str):
		return (await get(key)) is not None
	
	async def getall():
		ans={}
		for x in await tryrun(repldb.keys):
			ans[x]=await get(x)
		return ans