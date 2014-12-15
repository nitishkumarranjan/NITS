class Item():

    

    def __init__(self, name, image, cost, category):

        self.name = name
        self.image = image

        self.cost = cost
        self.category = category



    def changeCost(self, newCost):

        self.cost = newCost

    def printAll(self):
        print("Name : ",self.name)
        print("Cost : ",self.cost)
