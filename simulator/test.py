import LLM.formatter.parser as Parser
from engine.classes.agent import Agent
from brain.core.npc import NPC
from engine.core.world import World
from engine.actions.action import Action
import engine.actions.actionManager as ActionManager
from engine.classes.item import Item
from engine.classes.location import Location
from brain.state.personality.personalityModule import PersonalityModule
from engine.enums.degree import Degree

world = World()

world.registerItem(Item(2, 'a mug of beer: costs 10 gold', 5, (0, 0, 0)))
world.registerItem(Item(3, 'a sword: costs 50 gold', 5, (0, 0, 0)))
world.registerItem(Item(4, 'tax returns: unsellable', 5, (0, 0, 0)))
world.registerItem(Item(7, 'a pile of dog excrement', 6, (0, 0, 0)))
world.registerItem(Item(8, 'a pouch of gold coins', 6, (0, 0, 0)))
world.registerAgent(Agent(False, 0, ("John", "Doe"), 5, (0, 0, 0), []))
world.registerAgent(NPC(1, ("Jane", "Doe"), 5, (0, 0, 0), [2, 3, 4], "You are a tavern owner. You have 1 son, 1 daughter, and 1 husband.", "You would like to make as much money as possible to support your family.", PersonalityModule(Degree.NEUTRAL, Degree.VERY_HIGH, Degree.NEUTRAL, Degree.NEUTRAL, Degree.VERY_LOW)))

world.registerLocation(Location(5, "Jane's Tavern", (0, 0, 0), [6]))
world.registerLocation(Location(6, "Storage Closet", (1, 0, 0), [5]))

world.getAgent(1).conversationStart(world.getAgent(0))

#print([elem.getName() + ", " + str(elem.getParameters()) for elem in parser.parseFunctionList('attack(123)')])
#print([elem.getName() + ", " + str(elem.getParameters()) for elem in parser.parseFunctionList('say(\"hello there!\")')])
print(world.getInteractableAgents(0))

#world.emitAction(2, Action("SAY", ["Hello."], "", ActionManager.getDescription("SAY")))

while True:
    user = input('>>> ')

    action = None
    try:
        action = Parser.parseFunctionCall(user)
    except:
        action = Action("SAY", [user], "", ActionManager.getDescription("SAY"))
    
    world.emitAction(0, action)

