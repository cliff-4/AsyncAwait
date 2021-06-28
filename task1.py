import asyncio
import time
import aiohttp
import os

async def download_page(index):
	website = f"https://reqres.in/api/users?page{index}"
	
	file_name = "\\".join(( os.path.realpath(__file__).split("\\") )[0:-1]) + f"\\{index}.html"
	# this returns the file name of the output along with full path

	async with aiohttp.ClientSession() as session:
		async with session.get(website) as response:
			print(f"Status for {website}:", response.status)

			html = await response.read()
			# aiohttp works similar to requests. In this case, response.read() returns a byte string which can be written to a file
			
			with open(file_name, "wb") as file:
				file.write(html)
				file.close()

els = [1, 2, 3] #this is the list of the indices for the website to download

async def main():
	start = time.time()
	
	#a = download_page(els[0])
	#b = download_page(els[1])
	#c = download_page(els[2])
	#await asyncio.gather(a, b, c) #we can create three objects and gather then like this or we can use a list to pass them as arguments. Either works

	things = [download_page(el) for el in els]
	await asyncio.gather(*things)

	time_diff = time.time() - start
	print('Time Taken {0}'.format(time_diff))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

# individually awaiting results in tasks being executed after the previous task is over
# whereas using asyncio.gather(*args) starts all the tasks at once, greately improving execusion speed.
# best feature about this is that if the number of tasks increases, gather() outperforms single thread 
# performance by a significant performance, as can be see in task2.py
