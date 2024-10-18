from engine.classes.gameObject import GameObject

class Item(GameObject):
    def __init__(self, id: int, name: str, locationID: int, coordinates: tuple[float, float, float]) -> None:
        super().__init__(id, locationID, coordinates)
        self._name = name
    
    def getName(self):
        return self._name

    def getIdentifier(self) -> str:
        return 'Item(name: "{name}", id: {id})'.format(name=self._name, id=self.getID())
class ShopItem(GameObject):
    def __init__(self, id: int, name: str, price: int,locationID: int, coordinates: tuple[float, float, float]) -> None:
        super().__init__(id, locationID, coordinates)
        self._name = name
        self._price = price
    
    def getName(self):
        return self._name
    
    def getPrice(self):
        return self._price
    
    def getLocationID(self):
        return self._locationID
    
    def getID(self):
        return self._id
    
    def getCoordinates(self):
        return self._position
    
    def getIdentifier(self) -> str:
        return 'Item(name: "{name}", price: {price} coins, id: {id})'.format(name=self._name, price = self._price, id=self.getID())