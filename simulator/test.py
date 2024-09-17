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
#world.registerAgent(NPC(2, ("Joe", "Tavernowner"), (0, 0, 0)))

world.registerLocation(Location(5, "Jane's Tavern", (0, 0, 0), [6]))
world.registerLocation(Location(6, "Storage Closet", (1, 0, 0), [5]))

world.getAgent(1).conversationStart(world.getAgent(0))

#print([elem.getName() + ", " + str(elem.getParameters()) for elem in parser.parseFunctionList('attack(123)')])
#print([elem.getName() + ", " + str(elem.getParameters()) for elem in parser.parseFunctionList('say(\"hello there!\")')])
print(world.getInteractableAgents(0))

while True:
    user = input('>>> ')

    try:
        action = Parser.parseFunctionCall(user)
        world.emitAction(0, action)
    except:
        world.emitAction(0, Action("SAY", [user], "", ActionManager.getDescription("SAY")))

from brain.state.beliefs.evidence import Evidence
from brain.state.beliefs.beliefModule import BeliefModule
import time

"""beliefModule = BeliefModule()
beliefModule.addEvidence(Evidence(time.time(), 0, "John likes apples."))
beliefModule.addEvidence(Evidence(time.time(), 0, "John said the king died last week."))
beliefModule.addEvidence(Evidence(time.time(), 0, "John hangs out with the king on Saturdays."))
beliefModule.addEvidence(Evidence(time.time(), 0, "Jane said she fed the king some cyanide."))
beliefModule.addEvidence(Evidence(time.time(), 1, "Jane said she saw a prince on Saturday."))
beliefModule.addEvidence(Evidence(time.time(), 1, "Joe is a cool person."))
beliefModule.addEvidence(Evidence(time.time(), 1, "Jane said she'd like to go out on a date with Joe."))
beliefModule.addEvidence(Evidence(time.time(), 1, "Joe said he has a sinus infection."))

print(beliefModule.believes("The king is dead."))"""

"""from brain.state.memories.summarizedMemory import Memory
from brain.state.memories.summarizedMemoryModule import MemoryModule

memoryModule = MemoryModule()
memoryModule.addMemory(Memory(time.time(), time.time(), [2, 0, 1], "John and Jane stopped by to order a beer."))
memoryModule.addMemory(Memory(time.time(), time.time(), [2, 0], "John talked he despises Jane."))
memoryModule.addMemory(Memory(time.time(), time.time(), [2, 1], "Jane talked about how she loves John."))
memoryModule.addMemory(Memory(time.time(), time.time(), [2], "The king stopped by to say how much he loves this tavern."))
memoryModule.addMemory(Memory(time.time(), time.time(), [2], "The king ordered his guards to kill my child."))
memoryModule.addMemory(Memory(time.time(), time.time(), [2], "I am out of money, and my tavern will close soon."))
memoryModule.addMemory(Memory(time.time(), time.time(), [2, 1], "Jane said that she needs the money she loaned me by Saturday, but I already spent it all gambling."))
memoryModule.addMemory(Memory(time.time(), time.time(), [2], "I once killed Jane's dog because it annoyed me. She definitely overreacted a bit."))

print(memoryModule.remember("Who is Jane?"))"""



