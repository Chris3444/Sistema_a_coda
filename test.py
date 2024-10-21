import simpy 
import random 
import time      
from numpy import random 
import plotly.express as px #? matplotlib 
import asyncio #chemicke (events & queue)

mu = 5
queue = asyncio.Queue()

#Producer for mu packet per second
async def packet_creator(mu):
    counter = 0
    while True:
        await asyncio.sleep(random.poisson(1/mu))
        packet = counter
        await queue.put(packet)
        print(f"Created packet {packet}")

