import random 
import time      
from numpy import random 
import asyncio #whatmickis (events & queue)
from packet import Packet

y = 50
mu = 2
c = 20
queue = asyncio.Queue()
packet_array = []

def getMedianTime(packet_array):
    tot_time = 0
    for packet in packet_array:
        tot_time += packet.getTotTime()
    return tot_time/len(packet_array)

def getMediumQueueTime(packet_array):
    tot_time = 0
    for packet in packet_array:
        tot_time += packet.getQueueTime()
    return tot_time/len(packet_array)

#Producer for mu packet per second
async def packet_creator(y):
    initial_time = time.time()
    counter = 0
    while True:
        #random medium time to create a packet 
        await asyncio.sleep(random.poisson(1/y))
        packet = Packet(counter, initial_time)
        #put packet in queue
        await queue.put(packet)
        print(f"Created packet {packet.getID()}")
        counter += 1

#Server that process packet with rate y
async def server(mu, server_id):
    while True:
        
        #get packet from queue
        packet = await queue.get()
        packet.setQueueTime(time.time())
        #random medium time to process a packet
        await asyncio.sleep(random.poisson(1/mu))
        packet.setDepartureTime(time.time())
        print(f"Server: {server_id} processed packet: {packet.getID()} with service time: {packet.getServiceTime()} and queuTime: {packet.getQueueTime()}")
        packet_array.append(packet)
        

async def main():
    #start producer and server
    
    packet_creator_task = asyncio.create_task(packet_creator(y))
    server_task = [asyncio.create_task(server(mu, i+1)) for i in range(c)]
    
    #time of simulation
    await asyncio.sleep(30)
    #cancel producer and server
    packet_creator_task.cancel()
    queuesize = queue.qsize()
    for task in server_task:
        task.cancel()
    print("Simulation ended with ", len(packet_array), " packets processed and there are ", queuesize, " packets in queue")
    print("The average time a packet spends in the system is: ", getMedianTime(packet_array))
    print("The average time a packet spends in the queue is: ", getMediumQueueTime(packet_array))
asyncio.run(main())



