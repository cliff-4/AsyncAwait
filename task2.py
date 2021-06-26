import asyncio
import time
import aiohttp
import os
import json

def avg(list_object):
	a = 0
	for item in list_object:
		a += item
	a/= len(list_object)
	return round(a, 2)


async def sleep_coro(duration):
	await asyncio.sleep(duration)

async def download_page(index):
	#website = f"https://reqres.in/api/users?page{{{index}}}"
	website = f"https://xkcd.com/{index}/info.0.json"

	file_name = "\\".join((os.path.realpath(__file__).split("\\"))[0:-1]) + f"\\xkcd\\{index}.json"


	async with aiohttp.ClientSession() as session:
		async with session.get(website) as response:
			if response.status in range(200, 300):
				json_content = await response.json()
				json_text = json.dumps(json_content, indent = 4)
				
				with open(file_name, "w") as file:
					file.write(json_text)
					file.close()

async def main(n):
	files = ["\\".join((os.path.realpath(__file__).split("\\"))[0:-1]) + f"\\xkcd\\{i}.json" for i in range(1, 201)]
	for i in range(n):

		for file in files: os.remove(file)
		#sync downloading
		start = time.time()
		for el in els:
			await download_page(el)
		time_diff = time.time() - start
		sync_times.append(time_diff)

		for file in files: os.remove(file)
		#async downloading
		start = time.time()
		things = [download_page(el) for el in els]
		await asyncio.gather(*things)
		time_diff = time.time() - start
		async_times.append(time_diff)

times = 100
els = range(1, 201)
async_times = []
sync_times = []

loop = asyncio.get_event_loop()
loop.run_until_complete(main(times))

print(f"\nResult for {times} runs:\nAsync time avg: {avg(async_times)} s\nSync time avg: {avg(sync_times)} s\n")

#result for main(10): 
#	Async time avg: 1.77 s
#	Sync time avg: 20.9 s
# 	(sync takes 10.8 times more time to execute)
