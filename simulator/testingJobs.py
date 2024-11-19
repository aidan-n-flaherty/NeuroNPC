import LLM.parser.parser as Parser          #This is how LLM output is parsed
import LLM.formatter.formatter as Formatter #This is where LLM outpput is formated
from engine.classes.agent import Agent      #This is the User
from brain.core.npc import NPC              #This is the NPC
from brain.core.npcJob import Jobs          #NPC Jobs Object
from brain.core.npcJob import AutoJobs      #npc that holds alot of jobs and can auto give the jobs
from engine.core.world import World         #This is where KnowledgeBases, NPCS, Items, locations are initiated
from engine.stimuli.notification import Notification
import engine.stimuli.notificationModule as NotificationModule
from engine.classes.item import Item
from engine.classes.item import ShopItem    #This is what I added to Test
from engine.classes.container import Container
from engine.classes.location import Location
from brain.state.personality.personalityModule import PersonalityModule
from engine.enums.degree import Degree
from engine.stimuli.actionType import ActionType
from threading import Thread
from time import sleep

def emitActionToClient():
    pass

#Create world onject
world = World(emitActionToClient)

#registerItem(Item Object) -- Item Object created by: Item(int ID, string name_and_cost, int location_of_item_ID, vector coordinate)
world.registerShopItem(ShopItem(2, 'a mug of beer', 10, 5, (0, 0, 0)))
world.registerShopItem(ShopItem(3, 'a sword', 50, 5, (0, 0, 0)))
world.registerItem(Item(4, 'tax returns: unsellable', 5, (0, 0, 0)))
world.registerShopItem(ShopItem(9,'health potion that restores all your health', 50, 5, (0, 0, 0)))
world.registerShopItem(ShopItem(10,'damage potion that kills everything it touches', 250, 5, (0, 0, 0)))

#make chest in storage closet(id:6)
world.registerContainer(Container(11,5,[7,8],False,'chest in Storage Closet',6,(0, 0, 0)))
#Put the below items in chest
world.registerItem(Item(7, 'a pile of dog excrement', 11, (0, 0, 0)))
world.registerItem(Item(8, 'a pouch of gold coins', 11, (0, 0, 0)))

#registerAgent(Agent or NPC object) -- Agent is user. NPC is another NPC. Always give user false, and 0 ID
#Usage- NPC(NPC ID, (firstName string, lastName string), Location ID, (Location vector), Description for LLM, PersonalityModule() )
world.registerAgent(Agent(False, 0, ("John", "Doe"), 5, (0, 0, 0), []))
world.registerAgent(NPC(1, ("Jane", "Doe"), 5, (0, 0, 0), [2, 3, 4, 9, 10], "You are a tavern owner. You have 1 son named <@145>, 1 daughter named <@325>, and 1 husband named <@874>.", "You would like to make as much money as possible to support your family.", PersonalityModule({ "kind": Degree.HIGH, "pacifist": Degree.VERY_HIGH, "funny": Degree.HIGH, "weird": Degree.ABOVE_AVERAGE }, [ ], [ ])))
world.registerAgent(NPC(13, ("John", "Doe"), 5, (0, 0, 0), [], "You are the husband of the tavern owner.", "You would like to make as much money as possible to support your family.", PersonalityModule({ "kind": Degree.HIGH, "pacifist": Degree.VERY_HIGH, "funny": Degree.HIGH, "weird": Degree.ABOVE_AVERAGE }, [ ], [ ])))
#registerLocation(Location object)
#Usage- Location(locationID int, Description string, vector location, array of connected locations)
world.registerLocation(Location(5, "Jane's Tavern", (0, 0, 0), [6]))
world.registerLocation(Location(6, "Storage Closet", (1, 0, 0), [5,11]))
world.registerLocation(Location(11, "Coal Mine", (2, 0, 0), [6]))

unemployed = Jobs() #give this to agents that are unemployed

coal_mine_worker = Jobs("Coal Miner","Works in the local coal mine for 12 hours a day",[11],Degree.VERY_LOW,Degree.ABOVE_AVERAGE,Degree.VERY_HIGH)

emptyDict = dict()
dictOfAllJobs = dict()  #dict of a bunch of jobs. Key: number Index, Value: Tuple
dictOfAllJobs[0] = ("Coal Miner","Works in the local coal mine for 12 hours a day",[11])
dictOfAllJobs[1] = ("Coal Mine Manager","Manages the coal mine workers for 8 hours a day",[11])

autoJobsTest1 = AutoJobs(dictOfAllJobs) #First autoJob test object

autoJobsTest2 = AutoJobs(emptyDict)     #secound autoJob test Object
autoJobsTest2.addJob("Coal Miner","Works in the local coal mine for 12 hours a day",[11])
autoJobsTest2.addJob("Coal Mine Manager","Manages the coal mine workers for 8 hours a day",[11])

# these are both autojob objects with one job

randomJob1 = Jobs(autoJobsTest1)    #first test to see if a job was auto assigned
randomJob2 = Jobs(autoJobsTest2)    #secound test to see if a job was auto assigned

#input job into the changeJob function to see if it works
#either put in unemployed, randomJob1, or randomJob2
world.getAgent(1).changeJob(unemployed)
world.getAgent(13).changeJob(randomJob1)

world.getAgent(1).conversationStart(world.getAgent(0))

print(world.getInteractableAgents(0))

def tick():
    while True:
        world.tick()
        sleep(0.01)

thread = Thread(target=tick)
thread.start()

while True:
    user = input('>>> ') #ask user for text input

    action = None       # variable to store action 
    try:
        action = Parser.parseFunctionCall(user) #store user input in action
    except:
        action = Notification(ActionType("say"), [Formatter.formatTags(user, world)], "", NotificationModule.getDescription(ActionType("say"))) #turn user action into A notification object
    
    world.emitAction(0, action) #send to every NPC


