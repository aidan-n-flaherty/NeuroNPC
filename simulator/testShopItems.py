import LLM.parser.parser as Parser          #This is how LLM output is parsed
import LLM.formatter.formatter as Formatter #This is where LLM outpput is formated
from engine.classes.agent import Agent      #This is the User
from brain.core.npc import NPC              #This is the NPC
from engine.core.world import World         #This is where KnowledgeBases, NPCS, Items, locations are initiated
from engine.stimuli.notification import Notification
import engine.stimuli.notificationModule as NotificationModule
from engine.classes.item import Item
from engine.classes.item import ShopItem    #This is what I added to Test
from engine.classes.location import Location
from brain.state.personality.personalityModule import PersonalityModule
from engine.enums.degree import Degree
from engine.stimuli.actionType import ActionType

#Create world onject
world = World()

#registerItem(Item Object) -- Item Object created by: Item(int ID, string name_and_cost, int location_of_item_ID, vector coordinate)
world.registerItem(ShopItem(2, 'a mug of beer', 10, 5, (0, 0, 0)))
world.registerItem(ShopItem(3, 'a sword', 50, 5, (0, 0, 0)))
world.registerItem(Item(4, 'tax returns: unsellable', 5, (0, 0, 0)))
world.registerItem(Item(7, 'a pile of dog excrement', 6, (0, 0, 0)))
world.registerItem(Item(8, 'a pouch of gold coins', 6, (0, 0, 0)))
world.registerShopItem(ShopItem(9,'health potion that restores all your health', 50, 5, (0, 0, 0)))
world.registerShopItem(ShopItem(10,'damage potion that kills everything it touches', 250, 5, (0, 0, 0)))

#registerAgent(Agent or NPC object) -- Agent is user. NPC is another NPC. Always give user false, and 0 ID
#Usage- NPC(NPC ID, (firstName string, lastName string), Location ID, (Location vector), Description for LLM, PersonalityModule() )
world.registerAgent(Agent(False, 0, ("John", "Doe"), 5, (0, 0, 0), []))
world.registerAgent(NPC(1, ("Jane", "Doe"), 5, (0, 0, 0), [2, 3, 4], "You are a tavern owner. You have 1 son named <@145>, 1 daughter named <@325>, and 1 husband named <@874>.", "You would like to make as much money as possible to support your family.", PersonalityModule(Degree.VERY_LOW, Degree.VERY_HIGH, Degree.VERY_LOW, Degree.VERY_HIGH, Degree.NEUTRAL)))

#registerLocation(Location object)
#Usage- Location(locationID int, Description string, vector location, array of connected locations)
world.registerLocation(Location(5, "Jane's Tavern", (0, 0, 0), [6]))
world.registerLocation(Location(6, "Storage Closet", (1, 0, 0), [5]))

world.getAgent(1).conversationStart(world.getAgent(0))

print(world.getInteractableAgents(0))



while True:
    user = input('>>> ') #ask user for text input

    action = None       # variable to store action 
    try:
        action = Parser.parseFunctionCall(user) #store user input in action
    except:
        action = Notification(ActionType("say"), [Formatter.formatTags(user, world)], "", NotificationModule.getDescription(ActionType("say"))) #turn user action into A notification object
    
    world.emitAction(0, action) #send to every NPC


