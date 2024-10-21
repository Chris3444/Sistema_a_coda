import random 
import time      
from numpy import random 
import asyncio #whatmickis (events & queue)
from packet import Packet

mu = 3
y = 1
c = 4
queue = asyncio.Queue()

#Producer for mu packet per second
async def packet_creator(mu):
    initial_time = time.time()
    counter = 0
    while True:
        #random medium time to create a packet 
        await asyncio.sleep(random.poisson(1/mu))
        packet = Packet(counter, initial_time)
        #put packet in queue
        await queue.put(packet)
        print(f"Created packet {packet.getID()}")
        counter += 1

#Server that process packet with rate y
async def server(y, server_id):
    while True:
        
        #get packet from queue
        packet = await queue.get()
        packet.setQueueTime(time.time())
        #random medium time to process a packet
        await asyncio.sleep(random.poisson(1/y))
        print(f"Server: {server_id} processed packet: {packet.getID()}")
        packet.setServiceTime(time.time())

async def main():
    #start producer and server
    
    packet_creator_task = asyncio.create_task(packet_creator(mu))
    server_task = [asyncio.create_task(server(y, i+1)) for i in range(c)]
    
    #time of simulation
    await asyncio.sleep(60)
    #cancel producer and server
    packet_creator_task.cancel()
    for task in server_task:
        task.cancel()
    
asyncio.run(main())