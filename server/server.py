from gevent import monkey; monkey.patch_all()

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
from engine.stimuli.eventType import EventType
import time
from threading import Thread
from time import sleep
import json

from flask import Flask, Response, request, jsonify
from flask_sock import Sock
from werkzeug.wrappers import Request, Response, ResponseStream

from gevent.pywsgi import WSGIServer

worlds = {}

#world.emitAction(2, Action("SAY", ["Hello."], "", ActionManager.getDescription("SAY")))

# Eventually need to add function for exporting and importing world data and conversation history 

class middleware():
    '''
    Simple WSGI middleware
    '''


    #To-do: add export and authentication system
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        
        return self.app(environ, start_response)
            

        # res = Response(u'Authorization failed', mimetype= 'text/plain', status=401)
        # return res(environ, start_response)

app = Flask(__name__)
app.config['SOCK_SERVER_OPTIONS'] = {'ping_interval': 25}
sockets = Sock(app)

app.wsgi_app = middleware(app.wsgi_app)

#Register world route
@app.route("/auth", methods=['POST'])
def auth():
    if request.method == 'POST':
        # Handle POST request
        posted_data = request.get_json()  # Retrieve JSON data from the request
        data = {'message': 'This is a POST request', 'received': posted_data}
        return jsonify(data)

@sockets.route('/')
def websocket(ws):
    print('Received websocket connection')
    clients.append(ws)

    while True:
        data = ws.receive()
        if data == 'close':
            clients.remove(ws)
            break

def emitActionToClient(agentID: int, action: Notification):
    with app.app_context():
        for client in clients:
            client.send(json.dumps({
                'agentID': agentID,
                'action': {
                    'actionType': action.getType(),
                    'parameters': action.getParameters()
                }
            }) + '<|action_division|>')

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

worlds[0] = world

def tick():
    while True:
        worlds[0].tick()
        sleep(0.01)

thread = Thread(target=tick)
thread.start()

clients = []


@app.route('/registerAgent', methods=['POST'])
def registerAgent():
    if request.method == 'POST':
        data = request.get_json()
        
        worldID = data['worldID']
        agent = data['agent']
        world = worlds[worldID]

        world.registerAgent(Agent(agent['artificial'], agent['id'], agent['name'], agent['locationID'], agent['coordinates'], agent['inventory']))

        return jsonify({
            "status": "success"
        })
    else:
        return jsonify({
            "status": "method does not exist"
        })

@app.route('/registerItem', methods=['POST'])
def registerItem():
    if request.method == 'POST':
        data = request.get_json()
        
        worldID = data['worldID']
        item = data['item']
        world = worlds[worldID]

        world.registerItem(Item(item['id'], item['name'], item['locationID'], item['coordinates']))

        return jsonify({
            "status": "success"
        })
    else:
        return jsonify({
            "status": "method does not exist"
        })

@app.route('/setLocation', methods=['POST'])
def setLocation():
    if request.method == 'POST':
        data = request.get_json()
        
        worldID = data['worldID']
        location = data['location']
        world = worlds[worldID]

        world.registerLocation(Location(location['id'], location['name'], location['coordinates'], location['adjacent']))

        return jsonify({
            "status": "success"
        })
    else:
        return jsonify({
            "status": "method does not exist"
        })

@app.route('/setAgent', methods=['POST'])
def setAgent():
    if request.method == 'POST':
        data = request.get_json()
        
        worldID = data['worldID']
        world = worlds[worldID]

        if world.updateAgent(data['agent']):
            return jsonify({
                "status": "success"
            })
        else:
            return jsonify({
                "status": "could not update agent"
            })
    else:
        return jsonify({
            "status": "method does not exist"
        })

@app.route('/setItem', methods=['POST'])
def setItem():
    if request.method == 'POST':
        data = request.get_json()
        
        worldID = data['worldID']
        world = worlds[worldID]

        if world.updateItem(data['item']):
            return jsonify({
                "status": "success"
            })
        else:
            return jsonify({
                "status": "could not update item"
            })
    else:
        return jsonify({
            "status": "method does not exist"
        })

@app.route('/emitAction', methods=['POST'])
def emitAction():
    if request.method == 'POST':
        data = request.get_json()
        
        worldID = data['worldID']
        world = worlds[worldID]

        agentID = data['agentID']
        action = data['action']

        if not action['actionType'] in NotificationModule.getActions():
            return jsonify({
                "status": "action not registered"
            })

        actionType = ActionType(action['actionType'])

        if world.emitNotification(agentID, Notification(actionType, action['parameters'], descriptionStr=NotificationModule.getDescription(actionType))):
            return jsonify({
                "status": "success"
            })
        else:
            return jsonify({
                "status": "could not emit action"
            })
    else:
        return jsonify({
            "status": "method does not exist"
        })
    
@app.route('/emitEvent', methods=['POST'])
def emitEvent():
    if request.method == 'POST':
        data = request.get_json()
        
        worldID = data['worldID']
        world = worlds[worldID]

        sourceID = data['sourceID']
        event = data['event']

        if not event['eventType'] in NotificationModule.getEvents():
            return jsonify({
                "status": "action not registered"
            })

        eventType = EventType(event['eventType'])

        if world.emitNotification(sourceID, Notification(eventType, event['parameters'], descriptionStr=NotificationModule.getDescription(eventType))):
            return jsonify({
                "status": "success"
            })
        else:
            return jsonify({
                "status": "could not emit event"
            })
    else:
        return jsonify({
            "status": "method does not exist"
        })

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
    WSGIServer(('', 8080), app).serve_forever()
