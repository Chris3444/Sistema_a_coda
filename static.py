# EXTERNAL LIBRARY #
from numpy import random
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import unicodeit

# CUSTOM LIBRARY #
from Probability_functions import *


def static(): 
    k = 0  
    lamb = 13.89 #(ms)                                   # average arrival rate
    mu = 16.6  #(ms)                                   # average service rate
    c = 2   # number of servers
    rho = lamb / (c*mu)                               # server utilization
    A = c * rho                                       # traffic intensity
    P_queue = ErlangC(c, A)                         # probability of queueing
    print("P_queue: ", P_queue)
    
    Lq = P_queue * (rho/(1-rho))                  # average number of packets in the queue
    Lx = c * rho                                      # average number of customers in the system 
    Ls= Lq + Lx                                       # average number of packets in the system
    Ws = (ErlangC(c, c * rho) + c * (1 - rho)) / (mu * 30 * (1 - rho))                                     # average time a packet spends in the queue
    Wq = (ErlangC(c, c*rho)) / (mu* 30*(1-rho))
   # Ws = Ls / lamb   
   # Ws = Wq + (1/mu)                                    # average time a packet spends in the system
   # P_k = Pk(lamb, mu, k, c)

    print("Wq: ", Wq)
    print("Ws: ", Ws)
    print("LS: ", Ls)
    print("Lq: ", Lq)
   # print("Pk: ", P_k)
    test = random.poisson(mu, 100)

    print("")
    print(c*mu*Ws)

    # STATIC PARAMETERS
    rho_values = [i/100 for i in range(1, 100)]
    c_values = [1,2,3]

    # Ws AND Wq PLOT OVER RHO    
    Ws_values = [[],[],[]]
    Wq_values = [[],[],[]]
    for c in c_values:
        for rho in rho_values:
            Ws = (ErlangC(c, c * rho) + c * (1 - rho)) / (mu * 30 * (1 - rho))                                     # average time a packet spends in the queue
            Wq = (ErlangC(c, c*rho)) / (mu * 30 * (1 - rho))
            Ws_values[c-1].append(mu * 30 * Ws)
            Wq_values[c-1].append(mu * 30 * Wq)
    

    # Create the plot 
    time_plot = go.Figure()
    colors = ['blue', 'red', 'purple']  # Define a list of colors for different values of c
    for idx, c in enumerate(c_values):
        time_plot.add_trace(go.Scatter(x=rho_values, y=Ws_values[c-1], mode='lines', name=f'Ws, c = {c}', line=dict(color=colors[idx]), legendgroup='group1', legendgrouptitle_text='STATIC'))
        time_plot.add_trace(go.Scatter(x=rho_values, y=Wq_values[c-1], mode='lines', name=f"Wq, c = {c}", line=dict(color=colors[idx], dash='dash'), legendgroup='group1', legendgrouptitle_text='STATIC'))

    time_plot.update_layout(
        xaxis_title=unicodeit.replace("\\rho"),  # Use unicode to display the greek letter rho
        yaxis_title=unicodeit.replace("\\muWs,\\muWq"),
        legend_title="Legend",
        yaxis=dict(range=[0, 10])  # Set the y-axis range to have a maximum value of 10
    )
    #time_plot.show()

    # Ls AND Lq PLOT OVER RHO
    Ls_values = [[],[],[]]
    Lq_values = [[],[],[]]
    for c in c_values:
        for rho in rho_values:
            Lx = c * rho
            Lq = ErlangC(c, c*rho)  * (rho/(1-rho))
            Ls = ((ErlangC(c, c*rho) / (1 - rho)) + c)*rho  # average time a packet spends in the queue
            Ls_values[c-1].append(Ls)
            Lq_values[c-1].append(Lq)
    
    # Create the plot
    packets_plot = go.Figure()
    colors = ['blue', 'red', 'purple']  # Define a list of colors for different values of c
    for idx, c in enumerate(c_values):  
        packets_plot.add_trace(go.Scatter(x=rho_values, y=Ls_values[c-1], mode='lines', name=f'Ls, c = {c}', line=dict(color=colors[idx]), legendgroup='group1', legendgrouptitle_text='STATIC'))
        packets_plot.add_trace(go.Scatter(x=rho_values, y=Lq_values[c-1], mode='lines', name=f'Lq, c = {c}', line=dict(color=colors[idx], dash='dash'), legendgroup='group1', legendgrouptitle_text='STATIC'))

    packets_plot.update_layout(
        title="Ls and Lq over rho",
        xaxis_title="rho",
        yaxis_title=unicodeit.replace("Ls, Lq"),
        legend_title="Legend",
        yaxis=dict(range=[0, 10])  # Set the y-axis range to have a maximum value of 10
    )
    #packets_plot.show()

    # Pk PLOT OVER K
    packet_queue_plot = go.Figure()
    k = 5
    pK_values = [[],[],[]]
    for c in c_values:
        for i in range(k+1):
            pK_values[c-1].append(Pk(i, c, 0.5))   
        
    for i in range(3):  
        packet_queue_plot.add_trace(go.Bar(x=list(range(k + 1)), y= pK_values[i], name=f'P_queue, c = {i+1}', legendgroup='group1', legendgrouptitle_text='STATIC'))

    packet_queue_plot.update_layout(
        title="Pk over k",
        xaxis_title="k",
        yaxis_title="Pk",
        legend_title="Legend"
    )
    #packet_queue_plot.show()


    poisson = random.poisson(mu, 10000)
    packet_distribution = go.Figure()
    packet_distribution.add_trace(go.Histogram(x=poisson, histnorm='probability'))
    packet_distribution.update_layout(
        title="Poisson distribution of packets",
        title_x=0.5, 
        title_font=dict(size=22),
        xaxis_title="Packets",
        yaxis_title="Probability"
    )

    #packet_distribution.show()

    return {"packet_queue_plot": packet_queue_plot, "packets_plot": packets_plot, "time_plot": time_plot, "packet_distribution": packet_distribution}


STATIC_RESULTS = static()

