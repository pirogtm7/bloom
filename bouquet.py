import dbconnector as connector
class Bouquet:
    def __init__(self,bouquetId,price,description):
     self.bouquetId = bouquetId
     self.price = price
     self.description = description
     def get_bouquet_id(self):
      return bouquetId
     def get_price(self):
      return price
     def get_description(self):
        return description
n = connector.get_results()
print(n)
while(n != None):
 newBouquet = Bouquet(n[0],n[1],n[2])
print(newBouquet.price)

