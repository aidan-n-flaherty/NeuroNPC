from engine.classes.gameObject import GameObject
from engine.classes.item import Item

class Agent(GameObject):
    def __init__(self, artificial: bool, id: int, name: tuple[str, str], locationID: int, coordinates: tuple[float, float, float], inventory: list[int]) -> None:
        super().__init__(id, locationID, coordinates)
        self._name = name
        self._artificial = artificial
        self._inventory = inventory
    
    def update(self, coordinates: tuple[float, float, float], inventory: list[int]):
        self._position = coordinates
        self._inventory = inventory

    def isArtificial(self) -> bool:
        return self._artificial
    
    def getName(self) -> str:
        return " ".join(self._name) + " (id: {})".format(self.getID())
    
    def addItem(self, itemID: int) -> None:
        self._inventory.append(itemID)
    
    def removeObject(self, itemID: int) -> int:
        self._inventory.remove(itemID)

        return itemID
    
    def getInventory(self) -> list[int]:
        return self._inventory
    
    def getIdentifier(self) -> str:
        return '<Agent(name: "{name}", id:{id})>'.format(name=" ".join(self._name), id=self.getID())