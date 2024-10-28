import math

# implementazione della C di Erlang
def ErlangC(c, A): 
    intermezzo = (c / (c - A)) #valore parziale per il calcolo di numeratore e denominatore
    numeratore = (math.pow(A, c) / math.factorial(c)) * intermezzo
    
    risultato_sommatoria = 0
    for k in range(0, c - 1):
        risultato_sommatoria += (math.pow(A,k) / math.factorial(k)) 

    denominatore = risultato_sommatoria + ((math.pow(A,c) / math.factorial(c)) * intermezzo)

    return (numeratore / denominatore)