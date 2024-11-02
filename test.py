import random 
import time      
from numpy import random 
import asyncio #whatmickis (events & queue)
from packet import Packet
import plotly.express as px

from Probability_functions import *

lamb = 13.89 # (n) - packets/second           # average arrival rate
mu = 16.6 # (s) - packets/second           # average service rate
c = 2                                  # number of servers

queue = asyncio.Queue()
packet_array = []

packet_array_t = []

n_packet_queue_t = [] # add (queuesize) everi t time
# median = sumall(n_packet_queue_t) / len(array)

n_packet_sistem = [] # add (len (packet_array_t) ) rvery t time

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
        packet_array_t.append(packet)
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
        packet_array_t.pop()
        

async def getMediumPacket():
    while True:
        await asyncio.sleep(1)
        n_packet_sistem.append(len(packet_array_t))
        n_packet_queue_t.append(queue.qsize())


async def main():
    #start producer and server
    sim_time = 30
    packet_creator_task = asyncio.create_task(packet_creator(lamb))
    server_task = [asyncio.create_task(server(mu, i+1)) for i in range(c)]
    medium_packet_task = asyncio.create_task(getMediumPacket())
    
    #time of simulation
    await asyncio.sleep(sim_time)

    #cancel producer and server
    packet_creator_task.cancel()
    queuesize = queue.qsize()
    medium_packet_task.cancel()

    for task in server_task:
        task.cancel()


    #calculate medium number of packet in the queue
    queue_tot = 0
    for n in n_packet_queue_t:
        queue_tot += n
    mediumqueue = queue_tot / len(n_packet_queue_t)

    #calculate medium number of packet in the system
    packet_tot = 0
    for n in n_packet_sistem:
        packet_tot += n
    medium_packet = packet_tot / len(n_packet_sistem)


    print("Simulation ended with ", len(packet_array), " packets processed and there are ", queuesize, " packets in queue")
    print("The average time a packet spends in the system is: ", getMedianTime(packet_array))
    print("The average time a packet spends in the queue is: ", getMediumQueueTime(packet_array))    
    print("\n")
    print("The average number of packets in the queue is ", mediumqueue)
    print("The average number of packets in the system is ", medium_packet)

    import plotly.graph_objects as go

    # Calculate Ls and Lq over a range of rho values
    rho_values = [i/100 for i in range(1, 100)]
    Ls_values = []
    Lq_values = []

    for rho in rho_values:
        Ls = (lamb / mu) / (1 - (lamb / (c * mu)))
        Lq = Ls - (lamb / mu)
        Ls_values.append(Ls)
        Lq_values.append(Lq)

    # Create the plot
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=rho_values, y=Ls_values, mode='lines', name='Ls'))
    fig.add_trace(go.Scatter(x=rho_values, y=Lq_values, mode='lines', name='Lq'))

    fig.update_layout(
        title="Ls and Lq over rho",
        xaxis_title="rho",
        yaxis_title="Value",
        legend_title="Legend"
    )

    fig.show()

"""
    p_k_array = []
    for k in range(1,5):
        p_k_array(i) = Pk(lamb, mu, k, c)

    fig =  px.histogram(x = range(1,5), y = p_k_array, title="distribuzione")
    fig.show()   
"""
    
asyncio.run(main())



