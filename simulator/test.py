import LLM.parser.parser as Parser          #This is how LLM output is parsed
import LLM.formatter.formatter as Formatter #This is where LLM outpput is formated
from engine.classes.agent import Agent      #This is the User
from brain.core.npc import NPC              #This is the NPC
from engine.core.world import World         #This is where KnowledgeBases, NPCS, Items, locations are initiated
from engine.stimuli.notification import Notification
import engine.stimuli.notificationModule as NotificationModule
from engine.classes.item import Item
from engine.classes.location import Location
from brain.state.personality.personalityModule import PersonalityModule
from engine.enums.degree import Degree
from engine.stimuli.actionType import ActionType
from threading import Thread
from time import sleep


def emitActionToClient(agentID: int, agent):
    pass

#Create world onject
world = World(emitActionToClient)

#registerItem(Item Object) -- Item Object created by: Item(int ID, string name_and_cost, int location_of_item_ID, vector coordinate)
world.registerItem(Item(2, 'a mug of high quality beer: costs 10 gold', 5, (0, 0, 0)))
world.registerItem(Item(9, 'a mug of low quality disgusting beer: costs 10 gold', 5, (0, 0, 0)))
world.registerItem(Item(3, 'a sword: costs 50 gold', 5, (0, 0, 0)))
world.registerItem(Item(4, 'tax returns: unsellable', 5, (0, 0, 0)))
world.registerItem(Item(7, 'a pile of dog excrement', 6, (0, 0, 0)))
world.registerItem(Item(8, 'a pouch of gold coins', 6, (0, 0, 0)))
#registerAgent(Agent or NPC object) -- Agent is user. NPC is another NPC. Always give user false, and 0 ID
#Usage- NPC(NPC ID, (firstName string, lastName string), Location ID, (Location vector), Description for LLM, PersonalityModule() )
world.registerAgent(Agent(False, 0, ("John", "Doe"), 5, (0, 0, 0), []))
world.registerAgent(NPC(1, ("Jane", "Doe"), 5, (0, 0, 0), [2, 3, 4, 9], "You are a tavern owner. You have 1 son named <@145>, 1 daughter named <@325>, and 1 husband named <@874>.", "You would like to make as much money as possible to support your family.", PersonalityModule({ "kind": Degree.HIGH, "pacifist": Degree.VERY_HIGH, "funny": Degree.HIGH, "weird": Degree.ABOVE_AVERAGE }, [ "That's what my grandma always says!", "Exterminate the heathens!", "Cool beans!" ], [ "oops", "hehe", "howdy", "cool" ])))

#registerLocation(Location object)
#Usage- Location(locationID int, Description string, vector location, array of connected locations)
world.registerLocation(Location(5, "Jane's Tavern", (0, 0, 0), [6]))
world.registerLocation(Location(6, "Storage Closet", (1, 0, 0), [5]))

world.getAgent(1).conversationStart(world.getAgent(0))

#print([elem.getName() + ", " + str(elem.getParameters()) for elem in parser.parseFunctionList('attack(123)')])
#print([elem.getName() + ", " + str(elem.getParameters()) for elem in parser.parseFunctionList('say(\"hello there!\")')])
print(world.getInteractableAgents(0))

#world.emitAction(2, Notification("SAY", ["Hello."], "", NotificationModule.getDescription("SAY")))

def tick():
    while True:
        world.tick()
        sleep(0.01)

thread = Thread(target=tick)
thread.start()

while True:
    user = input('>>> ')

    action = None
    try:
        action = Parser.parseFunctionCall(user)
    except:
        action = Notification(ActionType("say"), [Formatter.formatTags(user, world)], "", NotificationModule.getDescription(ActionType("say")))
    
    world.emitNotification(0, action)


