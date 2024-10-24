import math

class GameObject:
    #Initilize game object
    def __init__(self, id: int, locationID: int, coordinates: tuple[float, float, float]) -> None:
        self._id = id
        self._position = coordinates
        self._locationID = locationID

    def getID(self):
        return self._id
    
    def getLocationID(self):
        return self._locationID
    
    def getPosition(self):
        return self._position
    
    def setPosition(self, position):
        self._position = position
    
    def canInteract(self, other: 'GameObject'):
        dX = other._position[0] - self._position[0]
        dY = other._position[1] - self._position[1]
        dZ = other._position[2] - self._position[2]

        return math.sqrt(dX * dX + dY * dY + dZ * dZ) < 100 and self._locationID == other._locationID
    
    def getIdentifier(self):
        return 'GameObject(id: {id})'.format(id=self._id)