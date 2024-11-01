import LLM.parser.parser as Parser          #This is how LLM output is parsed
import LLM.formatter.formatter as Formatter #This is where LLM outpput is formated
from engine.classes.agent import Agent      #This is the User
from brain.core.npc import NPC              #This is the NPC
from engine.core.world import World         #This is where KnowledgeBases, NPCS, Items, locations are initiated
from engine.actions.action import Action
import engine.actions.actionManager as ActionManager
from engine.classes.item import Item
from engine.classes.location import Location
from brain.state.personality.personalityModule import PersonalityModule
from engine.enums.degree import Degree
from engine.actions.actionType import ActionType
from flask import Flask, Response, request, jsonify
from flask_sockets import Sockets
import time



#world.emitAction(2, Action("SAY", ["Hello."], "", ActionManager.getDescription("SAY")))

# Eventually need to add function for exporting and importing world data and conversation history 

app = Flask(__name__)

@app.route("/")
def echo_socket(ws):
    #Create world object
    world = World()

    #registerItem(Item Object) -- Item Object created by: Item(int ID, string name_and_cost, int location_of_item_ID, vector coordinate)
    world.registerItem(Item(2, 'a mug of beer: costs 10 gold', 5, (0, 0, 0)))
    world.registerItem(Item(3, 'a sword: costs 50 gold', 5, (0, 0, 0)))
    world.registerItem(Item(4, 'tax returns: unsellable', 5, (0, 0, 0)))
    world.registerItem(Item(7, 'a pile of dog excrement', 6, (0, 0, 0)))
    world.registerItem(Item(8, 'a pouch of gold coins', 6, (0, 0, 0)))
    #registerAgent(Agent or NPC object) -- Agent is user. NPC is another NPC. Always give user false, and 0 ID
    #Usage- NPC(NPC ID, (firstName string, lastName string), Location ID, (Location vector), Description for LLM, PersonalityModule() )
    world.registerAgent(Agent(False, 0, ("John", "Doe"), 5, (0, 0, 0), []))
    world.registerAgent(NPC(1, ("Jane", "Doe"), 5, (0, 0, 0), [2, 3, 4], "You are a tavern owner. You have 1 son named <@145>, 1 daughter named <@325>, and 1 husband named <@874>.", "You would like to make as much money as possible to support your family.", PersonalityModule(Degree.VERY_LOW, Degree.VERY_HIGH, Degree.VERY_LOW, Degree.VERY_HIGH, Degree.NEUTRAL)))

    #registerLocation(Location object)
    #Usage- Location(locationID int, Description string, vector location, array of connected locations)
    world.registerLocation(Location(5, "Jane's Tavern", (0, 0, 0), [6]))
    world.registerLocation(Location(6, "Storage Closet", (1, 0, 0), [5]))

    world.getAgent(1).conversationStart(world.getAgent(0))

    #print([elem.getName() + ", " + str(elem.getParameters()) for elem in parser.parseFunctionList('attack(123)')])
    #print([elem.getName() + ", " + str(elem.getParameters()) for elem in parser.parseFunctionList('say(\"hello there!\")')])
    print(world.getInteractableAgents(0))
    while not ws.closed:
        message = ws.receive()
        ws.send(message)

@app.route('/item', methods=['GET', 'POST', 'DELETE'])
def item():
    if request.method == 'GET':
        # Handle GET request
        data = {'message': 'This is a GET request'}
        return jsonify(data)

    elif request.method == 'POST':
        # Handle POST request
        posted_data = request.get_json()  # Retrieve JSON data from the request
        data = {'message': 'This is a POST request', 'received': posted_data}
        return jsonify(data)
    elif request.method == 'DELETE':
        return
    
@app.route('/agent', methods=['GET', 'POST', 'DELETE'])
def agent():
    if request.method == 'GET':
        # Handle GET request
        data = {'message': 'This is a GET request'}
        return jsonify(data)

    elif request.method == 'POST':
        # Handle POST request
        posted_data = request.get_json()  # Retrieve JSON data from the request
        data = {'message': 'This is a POST request', 'received': posted_data}
        return jsonify(data)
    elif request.method == 'DELETE':
        return
    
@app.route('/location', methods=['GET', 'POST', 'DELETE'])
def location():
    if request.method == 'GET':
        # Handle GET request
        data = {'message': 'This is a GET request'}
        return jsonify(data)

    elif request.method == 'POST':
        # Handle POST request
        posted_data = request.get_json()  # Retrieve JSON data from the request
        data = {'message': 'This is a POST request', 'received': posted_data}
        return jsonify(data)
    elif request.method == 'DELETE':
        return

@app.route('/startConversation', methods=['POST'])
def startConversation():
    if request.method == 'GET':
        # Handle GET request
        data = {'message': 'This is a GET request'}
        return jsonify(data)

    elif request.method == 'POST':
        # Handle POST request
        posted_data = request.get_json()  # Retrieve JSON data from the request
        data = {'message': 'This is a POST request', 'received': posted_data}
        return jsonify(data)
    elif request.method == 'DELETE':
        return


if __name__ == '__main__':
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
