import math

def P0(rho, c): 
    res = 0
    k = 0
    while(True):
        temp1 = math.pow(c*rho, k) / math.factorial(k)
        temp2 = math.pow(c*rho, c) / math.factorial(c) 
        temp3 = 1 / (1 - rho)
        res += temp1 + (temp2 * temp3)
        
        k += 1
        if (k >= c - 1): 
            break

    return 1 / res 


def Pk(k, c, rho):
    P_0 = P0(rho, c)
    if k <= c:
        return P_0 * math.pow(c * rho, k) * (1 / math.factorial(k))
    else:
        return P_0 * math.pow(c * rho, k) * (1 / math.factorial(c) * math.pow(c, k-c))
    

# implementazione della C di Erlang
def ErlangC(c, A): 
    intermezzo = (1 / (1 - A/c)) #valore parziale per il calcolo di numeratore e denominatore
    numeratore = (math.pow(A, c) / math.factorial(c)) * intermezzo
    
    risultato_sommatoria = 0
    for k in range(0, c):
        risultato_sommatoria += (math.pow(A,k) / math.factorial(k)) 

    denominatore = risultato_sommatoria + ((math.pow(A,c) / math.factorial(c)) * intermezzo)

    return (numeratore / denominatore)

