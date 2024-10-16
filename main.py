# LIBRERIE ESTERNE #
import simpy 
import random 
import time      
import numpy
import plotly.express as px #? matplotlib 
import asyncio #chemicke

# LIBRERIE CUSTOM #
from ErlangC import ErlangC 

def main():    
    y = 100 #(ms)                                   # average arrival rate
    mu = 5  #(ms)                                   # average service rate
    c = int(input("Input number of servers:"))      # number of servers
    rho = y/(c*mu)                                  # server utilization
    A = c*rho                                       # traffic intensity
    P_queue = ErlangC(c, A)                         # probability of queueing
    print("P_queue: ", P_queue)
    
    Lq = P_queue * rho/(1-rho)                      # average number of packets in the queue
    Lx = c*rho                                      # TODO: trovare cosa sia Lx 
    Ls= Lq+Lx                                       # average number of packets in the system
    Wq = Lq/y                                       # average time a packet spends in the queue
    Ws = Ls/y                                       # average time a packet spends in the system

    
# TODO: implementare la visualizzazione dei risultati
#    fig =  px.bar(x=["Lq", "Lx", "Ls", "Wq", "Ws"], y=[Lq, Lx, Ls, Wq, Ws], title="Performance Measures")
#    fig.show()    


if __name__ == "__main__":
    main()