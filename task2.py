import asyncio
import time
import aiohttp
import os
import json

def avg(list_object): #function to calculate average of numbers in a list
	a = 0
	for item in list_object:
		a += item
	a/= len(list_object)
	return round(a, 2)

async def download_page(index):
	#website = f"https://reqres.in/api/users?page{{{index}}}"
	website = f"https://xkcd.com/{index}/info.0.json"

	file_name = "\\".join((os.path.realpath(__file__).split("\\"))[0:-1]) + f"\\xkcd\\{index}.json"
	# final file name along with full path.


	async with aiohttp.ClientSession() as session:
		async with session.get(website) as response:
			if response.status in range(200, 300):

				json_content = await response.json() 
				#response.read() returns a string, whereas response.json() returns a disctionary

				json_text = json.dumps(json_content, indent = 4)
				#the disctionary is then converted to a string with appropriate indentations
				
				with open(file_name, "w") as file:
					file.write(json_text)
					file.close()

async def main(n):
	files = ["\\".join((os.path.realpath(__file__).split("\\"))[0:-1]) + f"\\xkcd\\{i}.json" for i in range(1, 201)]
	# list of all the files created by task2.py

	for i in range(n):
		print(f"Run: {i+1}")

		for file in files: 
			try: os.remove(file) # deleting all files so it doesn't affect performance.
			except: 0

		#synchronous downloading
		start = time.time()
		for el in els:
			await download_page(el)
		time_diff = time.time() - start
		sync_times.append(time_diff) # adding results to an array to calculate average over multiple runs

		for file in files: 
			try: os.remove(file)
			except: 0

		#asynchronous downloading
		start = time.time()
		things = [download_page(el) for el in els]
		await asyncio.gather(*things)
		time_diff = time.time() - start
		async_times.append(time_diff)

times = 1 # number of runs
els = range(1, 201)
async_times = []
sync_times = []

loop = asyncio.get_event_loop()
loop.run_until_complete(main(times))

print(f"\nResult for {times} runs:\nAsync time avg: {avg(async_times)} s\nSync time avg: {avg(sync_times)} s\n")

# results:

# 	main( 1 ): 
#		Async time avg: 0.99 s
#		Sync time avg: 77.49 s
#		(sync takes 77.27 times more time to execute)

#	main( 1 ): 
#		Async time avg: 0.84 s
#		Sync time avg: 63.32 s
#		(sync takes 75.38 times more time to execute)

# 	main( 10 ): 
#		Async time avg: 1.77 s
#		Sync time avg: 20.9 s
# 		(sync takes 11.8 times more time to execute)

#	main( 10 ): 
#		Async time avg: 3.23 s
#		Sync time avg: 24.7 s
#		(sync takes 7.64 times more time to execute)

#	main( 10 ): 
#		Async time avg: 2.0 s
#		Sync time avg: 26.85 s
#		(sync takes 9.26 times more time to execute)

# 	main( 100 ): 
#		Async time avg: 3.39 s
#		Sync time avg: 29.29 s
# 		(sync takes 8.64 times more time to execute)

"""

It is noted that the first cycle takes significantly more time for the synchronous execution,
as compared to subsequent cycles, for some reason. But in the long run, async execution is about
10 times faster than sync execution. Of course, this number only increases as the number of 
requests per cycle increases.

"""