# EXTERNAL LIBRARY #
import time      
from numpy import random
#import plotly.express as px #? matplotlib 
import asyncio #whatmickis (events & queue)


# CUSTOM LIBRARY #
from ErlangC import ErlangC 
#TODO: Non è giusto Wq e Ws, son completamente sbagliati
def main():    
    y = 13.89 #(ms)                                   # average arrival rate
    mu = 16.6  #(ms)                                   # average service rate
    c = 2   # number of servers
    rho = y/(c*mu )                                # server utilization
    A = c * rho                                       # traffic intensity
    P_queue = ErlangC(c, A)                         # probability of queueing
    print("P_queue: ", P_queue)
    
    Lq = P_queue * (rho/(1-rho))                  # average number of packets in the queue
    Lx = c*rho                                      # average number of customers in the system 
    Ls= Lq+Lx                                       # average number of packets in the system
    Wq = Lq/y                                       # average time a packet spends in the queue
    Ws = Ls/y                                       # average time a packet spends in the system
    print("Wq: ", Wq)
    print("Ws: ", Ws)
    print("LS: ", Ls)
    print("Lq: ", Lq)
    test = random.poisson(mu, 100)

    print("\n")
    print(c*mu*Ws)
    
# TODO: implementare la visualizzazione dei risultati
# Visualizzazione poissoniana
#    fig =  px.histogram(test, title="distribuzione")
#    fig.show()    


if __name__ == "__main__":
    main()
