import time

class Packet:
    id = 0
    arrival_time = 0
    queue_time = 0
    service_time = 0
    departure_time = 0
    initial_time = 0 # Take the initial time of the simulation
    
    # CONSTRUCTOR #
    def __init__(self, id, initial_time):
        self.id = id
        self.arrival_time = time.time() - initial_time
        self.initial_time = initial_time

    # SETTERS #
    def setQueueTime(self, queue_time):
        self.queue_time = queue_time - self.initial_time - self.arrival_time

    def setDepartureTime(self, departure_time):
        self.departure_time = departure_time  - self.initial_time
        self.service_time = self.departure_time - self.queue_time - self.arrival_time

    # GETTERS #
    def getID(self):
        return self.id 

    def getQueueTime(self):
        return self.queue_time

    def getServiceTime(self):
        return self.service_time

    def getDepartureTime(self):
        return self.departure_time  

    def getTotTime(self):
        return self.departure_time - self.arrival_time
    
