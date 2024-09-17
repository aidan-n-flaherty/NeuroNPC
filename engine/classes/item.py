from engine.classes.gameObject import GameObject

class Item(GameObject):
    def __init__(self, id: int, name: str, locationID: int, coordinates: tuple[float, float, float]) -> None:
        super().__init__(id, locationID, coordinates)
        self._name = name
    
    def getName(self):
        return self._name

    def getIdentifier(self) -> str:
        return '<Item(name: "{name}", id: {id})>'.format(name=self._name, id=self.getID())