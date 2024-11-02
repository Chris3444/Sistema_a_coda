# EXTERNAL LIBRARY #
import time      
from numpy import random
import plotly.express as px #? matplotlib 
import asyncio #whatmickis (events & queue)


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
    
# TODO: implementare la visualizzazione dei risultati
# Visualizzazione poissoniana
#    fig =  px.histogram(test, title="distribuzione")
#    fig.show()    


if __name__ == "__main__":
    main()
