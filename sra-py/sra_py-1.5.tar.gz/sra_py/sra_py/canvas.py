import requests
import io
import aiohttp

SR = "https://some-random-api.ml/canvas/"

async def invert(avatar_url: str):
	async with aiohttp.ClientSession() as se:
		async with se.get(f"https://some-random-api.ml/canvas/invert?avatar={avatar_url}") as img:
			im = io.BytesIO(await img.read())
			await se.close()

	return im

async def wasted(avatar_url: str):
	async with aiohttp.ClientSession() as se:
		async with se.get(f"https://some-random-api.ml/canvas/wasted?avatar={avatar_url}") as img:
			im = io.BytesIO(await img.read())
			await se.close()

	return im

async def jail(avatar_url: str):
	async with aiohttp.ClientSession() as se:
		async with se.get(f"https://some-random-api.ml/canvas/jail?avatar={avatar_url}") as img:
			im = io.BytesIO(await img.read())
			await se.close()

	return im

async def mission_passed(avatar_url: str):
	async with aiohttp.ClientSession() as se:
		async with se.get(f"https://some-random-api.ml/canvas/passed?avatar={avatar_url}") as img:
			im = io.BytesIO(await img.read())
			await se.close()

	return im

async def glass(avatar_url: str):
	async with aiohttp.ClientSession() as se:
		async with se.get(f"https://some-random-api.ml/canvas/glass?avatar={avatar_url}") as img:
			im = io.BytesIO(await img.read())
			await se.close()

	return im

async def comrade(avatar_url: str):
	async with aiohttp.ClientSession() as se:
		async with se.get(f"https://some-random-api.ml/canvas/comrade?avatar={avatar_url}") as img:
			im = io.BytesIO(await img.read())
			await se.close()

	return im

async def simpcard(avatar_url: str):
	async with aiohttp.ClientSession() as se:
		async with se.get(f"https://some-random-api.ml/canvas/simpcard?avatar={avatar_url}") as img:
			im = io.BytesIO(await img.read())
			await se.close()

	return im

async def blur(avatar_url: str):
	async with aiohttp.ClientSession() as se:
		async with se.get(f"https://some-random-api.ml/canvas/blur?avatar={avatar_url}") as img:
			im = io.BytesIO(await img.read())
			await se.close()

	return im

async def pixelate(avatar_url: str):
	async with aiohttp.ClientSession() as se:
		async with se.get(f"https://some-random-api.ml/canvas/pixelate?avatar={avatar_url}") as img:
			im = io.BytesIO(await img.read())
			await se.close()

	return im

async def youtube_comment(username: str , comment: str , avatar_url: str):
	async with aiohttp.ClientSession() as se:
		async with se.get(f"https://some-random-api.ml/canvas/youtube-comment?username={username}&comment={comment.replace(' ' , '%20')}&avatar={avatar_url}") as img:
			im = io.BytesIO(await img.read())
			await se.close

	return im

async def its_so_stupid(avatar_url: str , text: str):
	async with aiohttp.ClientSession() as se:
		async with se.get(f"https://some-random-api.ml/canvas/its-so-stupid?avatar={avatar_url}&dog={text.replace(' ' , '%20')}") as img:
			im = io.BytesIO(await img.read())
			await se.close

	return im