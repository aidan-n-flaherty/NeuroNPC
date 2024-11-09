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
from flask import Flask, Response, request, jsonify
from flask_sockets import Sockets
from werkzeug.wrappers import Request, Response, ResponseStream
import time

worlds = {}


@app.route("/auth", methods=['POST'])
def auth():
    if request.method == 'POST':
        # Handle POST request
        posted_data = request.get_json()  # Retrieve JSON data from the request
        data = {'message': 'This is a POST request', 'received': posted_data}
        return jsonify(data)