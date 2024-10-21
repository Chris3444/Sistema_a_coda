import random 
import time      
from numpy import random 
import asyncio #chemicke (events & queue)

mu = 3
y = 1
c = 4
queue = asyncio.Queue()

#Producer for mu packet per second
async def packet_creator(mu):
    counter = 0
    while True:
        await asyncio.sleep(random.poisson(1/mu))
        packet = counter
        await queue.put(packet)
        print(f"Created packet {packet}")
        counter += 1

async def server(y, server_id):
    while True:
        packet = await queue.get()
        await asyncio.sleep(random.poisson(1/y))
        print(f"Server: {server_id} processed packet: {packet}")

async def main():
    packet_creator_task = asyncio.create_task(packet_creator(mu))
    server_task = [asyncio.create_task(server(y, i+1)) for i in range(c)]
    await asyncio.sleep(60)
    packet_creator_task.cancel()
    for task in server_task:
        task.cancel()
    
asyncio.run(main())