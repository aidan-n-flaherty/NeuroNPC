from engine.types.itemID import ItemID

class InventoryItemID(ItemID):
    @staticmethod
    def getGrammar(world, agentID):
        return '(' + ' | '.join(['"{}"'.format(itemID) for itemID in world.getAgent(agentID).getInventory()]) + ')'