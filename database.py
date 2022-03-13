# see documentation of replit.database here
# https://replit-py.readthedocs.io/en/latest/api.html
import setup


import asyncio
import logging

from aiohttp import ClientResponseError

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

						
from replit.database import AsyncDatabase
from replit import db
if db is not None:
	repldb=AsyncDatabase(db.db_url)
	
	class dberror(Exception):
		pass
	
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

elif setup.database=="local":
	print(setup.replurl)
	import os
	import aiohttp
	session=aiohttp.ClientSession()
	async def tryget(key:str):
		async with session.post(setup.replurl, json={"password":os.getenv("password"), "type": "get", "key": key}) as resp:
			return await resp.json()
	async def get(key:str):
		return tryrun(tryget, key)

	async def tryset(key:str, val):
		async with session.post(setup.replurl, json={"password":os.getenv("password"), "type": "set", "key": key, "val": val}) as resp:
			return await resp.json()
	async def set(key:str, val):
		return tryrun(tryset, key, val)

	async def trygetall():
		async with session.post(setup.replurl, json={"password":os.getenv("password"), "type": "getall"}) as resp:
			return await resp.json()
	async def getall():
		return await tryrun(trygetall)





	
