import asyncio
import time


# Define three coroutines that sleep for different durations
async def sleeper(duration, task_name=""):
    await asyncio.sleep(duration)
    return f"{task_name} slept for {duration} seconds"


# Create a list of coroutines
coros = [
    sleeper(4, task_name="task A"),
    sleeper(1, task_name="task B"),
    sleeper(2, task_name="task C"),
]


# Run the coroutines concurrently and get the results in the order they are completed
async def main():
    start = time.perf_counter()
    for coro in asyncio.as_completed(coros):
        # Wait for the result
        result = await coro
        print(f"Result: {result}")
    end = time.perf_counter()
    print(f"Elapsed time: {end - start}")


# Run the main coroutine
asyncio.run(main())