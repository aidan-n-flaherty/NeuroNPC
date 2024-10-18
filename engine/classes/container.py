from engine.classes.gameObject import GameObject

class Container(GameObject):
    def __init__(self, id: int, size: int, itemsInContainer: list, isLocked: bool, name: str,locationID: int, coordinates: tuple[float, float, float]) -> None:
        super().__init__(id, locationID, coordinates)
        self._name = name
        self._size = size
        self._isLocked = isLocked
        self._itemsInContainer = itemsInContainer

    def getLocationID(self):
        return self._locationID
    
    def getID(self):
        return self._id
    
    def getCoordinates(self):
        return self._position
    
    def getName(self):
        return self._name
    
    def getSize(self):
        return self._size
    
    def isLocked(self):
        return self._isLocked
    
    def getItemsInCointer(self):
        return self._itemsInContainer
    
    def isFull(self):
        return len(self._itemsInContainer) > self._size-1
    
    def setContainer(self, newItemArray: list):
        self._itemsInContainer = newItemArray

    def setLocked(self, value: bool):
        self._isLocked = value
    
    def getIdentifier(self) -> str:
        #If locked NPC not able to see IDS in container
        if(self.isLocked()):
            return 'Container(name: "{name}", list of item IDS in Container: "UNKNOWN: Container Locked", container is locked: "{isLocked}", id: {id})'.format(name=self._name, isLocked=self._isLocked, id = self.getID())
        #If Unlocked Npc can see the IDS in container
        else:
            return 'Container(name: "{name}", list of item IDS in Container: "{itemsInContainer}", container is locked: "{isLocked}", id: {id})'.format(name=self._name, itemsInContainer = self._itemsInContainer, isLocked=self._isLocked, id = self.getID())