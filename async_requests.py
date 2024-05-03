import asyncio
import aiohttp
import time

async def make_request(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    url = 'http://localhost:8080/home'
    num_requests = 10000

    start_time = time.time()  # Record start time

    async with aiohttp.ClientSession() as session:
        tasks = [make_request(session, url) for _ in range(num_requests)]
        responses = await asyncio.gather(*tasks)

        # Calculate total time taken
        end_time = time.time()
        total_time = end_time - start_time

        # You can process responses here if needed
        print(f"Received {len(responses)} responses")
        print(f"Total time taken: {total_time:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
