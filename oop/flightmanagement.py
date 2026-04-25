class user:
    def __init__(self, id, name):
        self._name = name 
        self._id = id
    
    def __str__(self):
        return f"{self._name}, {self._id}"

class pilot(user):
    def performrole(self):
        print(f"{self._name} is flying the plane")

class passenger(user):
    def performrole(self):
        print(f"{self._name} is traveling in seat 23A")

class flight:
    def __init__(self, pilot_obj, passengers, place):
        self.pilot = pilot_obj
        self.passengers = passengers
        self.place = place

    def jonure(self):
        print(f"Today flight to {self.place} with pilot {self.pilot._name}")
        print(f"Number of passengers: {len(self.passengers)}")

p1 = pilot(101, "captain jassim")
passengers_list = [passenger(1, "dania"), passenger(2, "adya")]

my_flight = flight(p1, passengers_list, "dubai")
my_flight.jonure()

p1.performrole()
for p in passengers_list:
    p.performrole()