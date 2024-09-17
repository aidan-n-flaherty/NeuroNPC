class LocationID(int):
    @staticmethod
    def getGrammar(world, agentID):
        return '(' + ' | '.join(['"{}"'.format(i) for i in world.getAccessibleLocations(agentID)]) + ')'