class vehicle :
      def __init__(self,brand,year):
            self.brand=brand
            self.year=year
      def yu(self):
            return f"{self.brand} is driving"
class car(vehicle):
      def honk(self):
            return print(f"{self.brand} say beeeeeb")
class bike(vehicle):
      def ball(self):
            return print(f"{self.brand} say ring ball")
c1=car("nq",34)
bi=bike("oi",33)
c1.yu()
c1.honk()
bi.ball()

