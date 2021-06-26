import asyncio
import time
import aiohttp
import os
import json

async def sleep_coro(duration):
	await asyncio.sleep(duration)

async def download_page(index):
	website = f"https://reqres.in/api/users?page{index}"

	file_name = "\\".join((os.path.realpath(__file__).split("\\"))[0:-1]) + f"\\{index}.html"
	async with aiohttp.ClientSession() as session:
		async with session.get(website) as response:
			print(f"Status for {website}:", response.status)

			html = await response.read()
			
			with open(file_name, "wb") as file:
				file.write(html)
				file.close()

els = [1, 2, 3]

async def main():
	start = time.time()
	a = download_page(els[0])
	b = download_page(els[1])
	c = download_page(els[2])

	#things = [download_page(el) for el in els]
	#await asyncio.gather(*things)
	await asyncio.gather(a, b, c)

	time_diff = time.time() - start
	print('Time Taken {0}'.format(time_diff))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
