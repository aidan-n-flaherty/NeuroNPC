from engine.classes.gameObject import GameObject

class Location(GameObject):
    def __init__(self, id: int, name: str, coordinates: tuple[float, float, float], adjacent: list[int]) -> None:
        self._id = id
        self._position = coordinates
        self._name = name
        self._adjacentLocationIDs = adjacent
    
    def getID(self):
        return self._id
    
    def getPosition(self):
        return self._position
    
    def setPosition(self, position):
        self._position = position
    
    def getName(self):
        return self._name
    
    def getAdjacentIDs(self):
        return self._adjacentLocationIDs

    def getIdentifier(self) -> str:
        return '<Location(name: "{name}", id: {id})>'.format(name=self._name, id=self.getID())