# EXTERNAL LIBRARY #
import random 
import time      
from numpy import random 
import asyncio #whatmickis (events & queue)
from packet import Packet
import plotly.graph_objects as go
import numpy as np

# CUSTOM LIBRARY #
from Probability_functions import *

# MEDIAN TIME FUNCTIONS #
def getMedianTime(packet_array):
    tot_time = 0
    for packet in packet_array:
        tot_time += packet.getTotTime()
    return tot_time/len(packet_array) if  len(packet_array) > 0 else 0

def getMediumQueueTime(packet_array):
    tot_time = 0
    for packet in packet_array:
        tot_time += packet.getQueueTime()
    return tot_time/len(packet_array) if  len(packet_array) > 0 else 0

async def getMediumPacket(queue,packet_all):
    while True:
        await asyncio.sleep(1)
        packet_all["n_packet_sistem"].append(len(packet_all["packet_array_t"]))
        packet_all["n_packet_queue_t"].append(queue.qsize())
        #n_packet_sistem.append(len(packet_array_t))
        #n_packet_queue_t.append(queue.qsize())


# QUEUE SYSTEM DEFINITION #
#Producer for mu packet per second
async def packet_creator(y,queue,packet_all):
    initial_time = time.time()
    counter = 0
    while True:
        #random medium time to create a packet 
        await asyncio.sleep(random.poisson(1/y))
        packet = Packet(counter, initial_time)
        packet_all["packet_array_t"].append(packet)
        #packet_array_t.append(packet)
        #put packet in queue
        if not queue.empty():
            packet_all["waiting_arrivals"] += 1
        await queue.put(packet)
        #print(f"Created packet {packet.getID()}")
        counter += 1

#Server that process packet with rate y
async def server(mu, server_id, queue,packet_all):
    while True:       
        #get packet from queue
        packet = await queue.get()
        packet.setQueueTime(time.time())
        #random medium time to process a packet
        await asyncio.sleep(random.poisson(1/mu))
        packet.setDepartureTime(time.time())
        #print(f"Server: {server_id} processed packet: {packet.getID()} with service time: {packet.getServiceTime()} and queuTime: {packet.getQueueTime()}")
        packet_all["packet_array"].append(packet)
        packet_all["packet_array_t"].pop()
        #packet_array.append(packet)
        #packet_array_t.pop()

# SIMULATIONS HANDLING #
def get_metrics(packet_all):

    #P_queue = packet_all["waiting_arrivals"] / len(packet_all["packet_array"]) if  len(packet_all["packet_array"]) > 0 else 0
    #P_queue = waiting_arrivals / len(packet_array) if  len(packet_array) > 0 else 0
    Lq = getMediumQueueTime(packet_all["packet_array"])
    Ls = getMedianTime(packet_all["packet_array"])
    #calculate medium number of packet in the queue
    queue_tot = 0
    for n in packet_all["n_packet_queue_t"]:
        queue_tot += n
    Wq = queue_tot / len(packet_all["n_packet_queue_t"]) if  len(packet_all["n_packet_queue_t"]) > 0 else 0
    #calculate medium number of packet in the system
    packet_tot = 0
    for n in packet_all["n_packet_sistem"]:
        packet_tot += n
    Ws = packet_tot / len(packet_all["n_packet_sistem"]) if  len(packet_all["n_packet_sistem"]) > 0 else 0
    # Calculate Pk for k = 1, 2, 3, 4, 5
    pk_counts = {k: 0 for k in range(6)}
    total_entries = len(packet_all["n_packet_sistem"])
    for count in packet_all["n_packet_sistem"]:
        if count in pk_counts:
            pk_counts[count] += 1

    # Convert counts to probabilities
    pK = {k: pk_counts[k] / total_entries for k in pk_counts}

    return {"Lq": Lq, "Ls": Ls, "Wq": Wq, "Ws": Ws, "Pk": pK}


async def createSim(lamb, mu, c, runtime):
    waiting_arrivals = 0

    packet_array = []

    packet_array_t = []

    n_packet_queue_t = [] # add (queuesize) everi t time
    # median = sumall(n_packet_queue_t) / len(array)

    n_packet_sistem = [] # add (len (packet_array_t) ) rvery t time
    packet_all = {"packet_array": packet_array, "packet_array_t": packet_array_t, "n_packet_queue_t": n_packet_queue_t, "n_packet_sistem": n_packet_sistem, "waiting_arrivals": waiting_arrivals}
    queue = asyncio.Queue()
    packet_creator_task = asyncio.create_task(packet_creator(lamb,queue,packet_all))
    server_task = [asyncio.create_task(server(mu, i+1,queue,packet_all )) for i in range(c)]
    medium_packet_task = asyncio.create_task(getMediumPacket(queue,packet_all))
    #time of simulation
    await asyncio.sleep(runtime)

    #cancel producer and server
    packet_creator_task.cancel()
    medium_packet_task.cancel()
    for task in server_task:
        task.cancel()
    results = get_metrics(packet_all)
    packet_array = []
    packet_array_t = []
    waiting_arrivals = 0
    n_packet_queue_t = [] # add (queuesize) everi t time
    # median = sumall(n_packet_queue_t) / len(array)

    n_packet_sistem = [] # add (len (packet_array_t) ) rvery t time
    return results


async def createSims(mu,c_values,rho_values,repetitions,runtime):
    results = {c: {rho: {} for rho in rho_values} for c in c_values}

    async def run_for_c_and_rho(c, rho):
        lamb = rho * c * mu

        # Run the simulation `repetitions` times concurrently for the current (c, rho) pair
        tasks = [createSim(lamb, mu, c, runtime) for _ in range(repetitions)]
        metrics_list = await asyncio.gather(*tasks)

        # Separate each metric and calculate the median across repetitions
        Lq_values = [metrics["Lq"] for metrics in metrics_list]
        Ls_values = [metrics["Ls"] for metrics in metrics_list]
        Wq_values = [metrics["Wq"]*mu*c for metrics in metrics_list]
        Ws_values = [metrics["Ws"]*mu*c for metrics in metrics_list]
        Pk_values = [metrics["Pk"] for metrics in metrics_list]
        # Populate Pk_aggregated with each Pk value from Pk_values
        Pk_aggregated = {k: [] for k in range(6)}
        for pk_dict in Pk_values:
            for k, value in pk_dict.items():
                Pk_aggregated[k].append(value)

        # Calculate median for each k
        Pk_median = {k: np.median(Pk_aggregated[k]) for k in Pk_aggregated}

        
        # Calculate and store median values for each metric
        results[c][rho] = {
            "Lq": np.median(Lq_values),
            "Ls": np.median(Ls_values),
            "Wq": np.median(Wq_values),
            "Ws": np.median(Ws_values),
            "Pk": Pk_median,
        }
    tasks = [run_for_c_and_rho(c, rho) for c in c_values for rho in rho_values]
    await asyncio.gather(*tasks)
    return results


# PLOTTING #
def plotResults(results, rho_values, c_values):
    # Prepare data for P_queue bar chart
    p_queue_data = []
    
    for c in c_values:
       
        p_queue_values = [results[c][0.5]["Pk"] for k in results[c][0.5]["Pk"]]
        pk_data= results[c][0.5]["Pk"]  # Convert dict_keys to a list
        x_values = list(pk_data.keys())  # k values
        y_values = list(pk_data.values())  # Pk values for the current `c`
        # Add a bar for this server configuration
        p_queue_data.append(go.Bar(name=f'Servers = {c}', x=x_values, y=y_values))
        # Prepare data for Lq and Ls scatter plot
    lq_ls_data = []
    for c in c_values:
        lq_values = [results[c][rho]["Lq"] for rho in rho_values]
        ls_values = [results[c][rho]["Ls"] for rho in rho_values]
        
        # Add Lq and Ls as separate traces for each `c`
        lq_ls_data.append(go.Scatter(name=f'Lq (Servers = {c})', x=rho_values, y=lq_values, mode='lines+markers'))
        lq_ls_data.append(go.Scatter(name=f'Ls (Servers = {c})', x=rho_values, y=ls_values, mode='lines+markers'))

    # Prepare data for Wq and Ws scatter plot
    wq_ws_data = []
    for c in c_values:
        wq_values = [results[c][rho]["Wq"] for rho in rho_values]
        ws_values = [results[c][rho]["Ws"] for rho in rho_values]
        
        # Add Wq and Ws as separate traces for each `c`
        wq_ws_data.append(go.Scatter(name=f'Wq (Servers = {c})', x=rho_values, y=wq_values, mode='lines+markers'))
        wq_ws_data.append(go.Scatter(name=f'Ws (Servers = {c})', x=rho_values, y=ws_values, mode='lines+markers'))

    # Create the bar chart for P_queue
    fig1 = go.Figure(data=p_queue_data)
    fig1.update_layout(
        title="Probability of Packets(Pk) in Packets (k)",
        xaxis_title="Packets (k)",
        yaxis_title="Pk",
        barmode='group'
    )

    # Create the scatter plot for Lq and Ls
    fig2 = go.Figure(data=lq_ls_data)
    fig2.update_layout(
        title="Average Queue Length (Lq) and System Length (Ls) vs Utilization (rho)",
        xaxis_title="Utilization (rho)",
        yaxis_title="Lq, Ls"
    )

    # Create the scatter plot for Wq and Ws
    fig3 = go.Figure(data=wq_ws_data)
    fig3.update_layout(
        title="Average Waiting Time in Queue (Wq) and System (Ws) vs Utilization (rho)",
        xaxis_title="Utilization (rho)",
        yaxis_title="Wq, Ws"
    )

    # Show the plots
    fig1.show()
    return [fig2,fig3]


# MAIN #
async def main():
    mu = 4 # (s) - packets/second           # average service rate
    c_values = [1,2,3]                               # number of servers
    repetitions = 10
    runtime = 60
    rho_values = [round(0.01*i,1) for i in range(1,100)]                              
    results = await createSims(mu,c_values, rho_values,repetitions,runtime)
    print("finished")
    for c in results:
        for rho in results[c]:
            #print(f"Servers: {c}, Utilization: {rho}, Metrics: {results[c][rho]}")
            hello = 0
    figs = plotResults(results, rho_values, c_values)

asyncio.run(main())



