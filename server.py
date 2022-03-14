from aiohttp import web
from aiohttp.web import Response,json_response
from utils import verify_password
import database as db
import os

app = web.Application()
routes = web.RouteTableDef()

@routes.get("/")
async def homepage(req):
	return Response(text="hello world")

@routes.post("/db")
async def database_request(req):
	data=await req.json()
	if verify_password(data["password"], os.getenv("password_hash")):
		if data["type"]=="get":
			ans=await db.get(data["key"])
		elif data["type"]=="set":
			ans=await db.set(data["key"],data["val"])
		elif data["type"]=="getall":
			ans=await db.getall()
		return json_response(ans)

from utils import generate_password, hash_password
@routes.get("/generate")
async def generate(req):
	pwd=generate_password()
	return Response(text=f"password=\n{pwd}\n\n\npassword_hash=\n{hash_password(pwd)}")


async def startserver():
	app.add_routes(routes)
	runner = web.AppRunner(app)
	await runner.setup()
	site = web.TCPSite(runner, '0.0.0.0', 8080)
	await site.start()