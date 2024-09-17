class AgentID(int):
    @staticmethod
    def getGrammar(world, agentID):
        return '(' + ' | '.join(['"{}"'.format(i) for i in world.getInteractableAgents(agentID)]) + ')'