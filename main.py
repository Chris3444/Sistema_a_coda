# EXTERNAL LIBRARY #
import time      
from numpy import random
import plotly.express as px #? matplotlib 
import asyncio #whatmickis (events & queue)

import plotly.graph_objects as go
# CUSTOM LIBRARY #
from Probability_functions import *

#TODO: Non è giusto Wq e Ws, son completamente sbagliati
def main(): 
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
    fig = go.Figure()
    for c in c_values:  
        fig.add_trace(go.Scatter(x=rho_values, y=Ws_values[c-1], mode='lines', name=f'Ws, c = {c}'))
        fig.add_trace(go.Scatter(x=rho_values, y=Wq_values[c-1], mode='lines', name=f'Wq, c = {c}'))

    fig.update_layout(
        title="Ws and Wq over rho",
        xaxis_title="rho",
        yaxis_title="Value",
        legend_title="Legend"
    )
    # fig.show()

    # Ls AND Lq PLOT OVER RHO
    Ls_values = [[],[],[]]
    Lq_values = [[],[],[]]
    for c in c_values:
        for rho in rho_values:
            Lx = c * rho
            Lq = ErlangC(c, c*rho)  * (rho/(1-rho))
            Ls = ((ErlangC(c, c*rho) / (1 - rho)) + c)*rho                                    # average time a packet spends in the queue
            Ls_values[c-1].append(Ls)
            Lq_values[c-1].append(Lq)
    
    # Create the plot
    fig2 = go.Figure()
    for c in c_values:  
        fig2.add_trace(go.Scatter(x=rho_values, y=Ls_values[c-1], mode='lines', name=f'Ls, c = {c}'))
        fig2.add_trace(go.Scatter(x=rho_values, y=Lq_values[c-1], mode='lines', name=f'Lq, c = {c}'))

    fig2.update_layout(
        title="Ls and Lq over rho",
        xaxis_title="rho",
        yaxis_title="Value",
        legend_title="Legend"
    )
    # fig2.show()

    # Pk PLOT OVER K
    fig3 = go.Figure()
    k = 5
    pK_values = [[],[],[]]
    for c in c_values:
        for i in range(k+1):
            pK_values[c-1].append(Pk(lamb, mu, i, c, 0.5))
    
        
    for i in range(3):  
        fig3.add_trace(go.Bar(x=list(range(k + 1)), y= pK_values[i], name=f'P_queue, c = {i+1}'))

    fig3.update_layout(
        title="Pk over k",
        xaxis_title="k",
        yaxis_title="Pk",
        legend_title="Legend"
    )
    
    fig3.show()


# TODO: implementare la visualizzazione dei risultati
# Visualizzazione poissoniana
#    fig =  px.histogram(test, title="distribuzione")
#    fig.show()    


if __name__ == "__main__":
    main()
