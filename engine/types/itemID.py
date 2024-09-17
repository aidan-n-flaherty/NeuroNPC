class ItemID(int):
    @staticmethod
    def getGrammar(world, agentID):
        return '(' + ' | '.join(['"{}"'.format(itemID) for itemID in world.getInteractableItems(agentID)]) + ')'