from brain.state.personality.personalityModule import PersonalityModule
from engine.enums.degree import Degree
from engine.core.world import World
from brain.core.npc import NPC 
from engine.classes.item import Item
from engine.classes.location import Location

world = World()

world.registerItem(Item(2, 'a mug of beer: costs 10 gold', 5, (0, 0, 0)))
world.registerItem(Item(3, 'a sword: costs 50 gold', 5, (0, 0, 0)))
world.registerItem(Item(4, 'tax returns: unsellable', 5, (0, 0, 0)))
world.registerItem(Item(7, 'a pile of dog excrement', 6, (0, 0, 0)))
world.registerItem(Item(8, 'a pouch of gold coins', 6, (0, 0, 0)))
world.registerLocation(Location(5, "Jane's Tavern", (0, 0, 0), [6]))
world.registerLocation(Location(6, "Storage Closet", (1, 0, 0), [5]))

world.registerAgent(NPC(1, ("Jane", "Doe"), 5, (0, 0, 0), [2, 3, 4], "You are a tavern owner. You have 1 son named <@145>, 1 daughter named <@325>, and 1 husband named <@874>.", "You would like to make as much money as possible to support your family.", PersonalityModule(Degree.VERY_LOW, Degree.VERY_HIGH, Degree.VERY_LOW, Degree.VERY_HIGH, Degree.NEUTRAL)))

while True:
    sentence = input(">>> ")
    world.getAgent(1)._behaviorModule.addPolicy(world.getAgent(1), sentence, world)