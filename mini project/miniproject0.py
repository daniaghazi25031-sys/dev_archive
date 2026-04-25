class bankaccount:
    def __init__(self,owner,balance):
        self.owner=owner
        self.__balance=balance
    def balance_get(self):
        return f"your balance is {self.__balance}"
    def withdrawn(self,amount):
        if amount> self.__balance:
           return print("sorry cant help u")
        else:
            self.__balance -=amount
            return f"your balance now is {self.__balance}"
    def deposit(self,amount):
        self.__balance+= amount
        return self.__balance
class savingaccount(bankaccount):
      def culculator(self):
          interest=self.balance_get()*0.05
          return interest
class currentaccount(bankaccount):
      def culculator(self):
          interest=self.balance_get()*0.01
          return interest
save=savingaccount("dania",1000)
current=currentaccount("jj",1200)
save.deposit(200)
current.withdrawn(30)
print("interest is=", save.balance_get(),current.balance_get())


