import os

from flask import Flask, render_template, request, session, jsonify
from flask_session import Session
from flask_socketio import SocketIO, emit
import datetime, time

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Configure session to use filesystem
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

#Some default channels
channels_data = {'general': [], 'cs': [], 'bio': [], 'history': [], 'art': []}

#Some sample messages
message1 = {'channel': 'general', 'timestamp': int(time.time()), 'username': 'Bill Gates', 'text' : 'This is a message from Bill Gates'}
message2 = {'channel': 'general', 'timestamp': int(time.time()), 'username': 'Steve Jobs', 'text' : 'This is a message from Steve Jobs'}
message3 = {'channel': 'cs', 'timestamp': int(time.time()), 'username': 'Elon Musk', 'text' : 'This is a message from Elon Must'}
message4 = {'channel': 'cs', 'timestamp': int(time.time()), 'username': 'Jeff Bezos', 'text' : 'This is a message from Jeff Bezos'}
message5 = {'channel': 'art', 'timestamp': int(time.time()) , 'username': 'Bruce Lee', 'text' : 'This is a message from Bruce Lee'}
channels_data['general'].append(message1)
channels_data['general'].append(message2)
channels_data['cs'].append(message3)
channels_data['cs'].append(message4)
channels_data['art'].append(message5)


num_messages_to_store = 100 # arbritrary number
selected_channel = 'general' # default starting channel


@app.route('/', methods = ['GET','POST'])
def index():
    return render_template('index.html')

@socketio.on('send message')
def sendMessage(message_data):
    #first we remove messages that exceed our 100 message limit
    while len(channels_data[message_data['channel']]) >= num_messages_to_store :
        channels_data[message_data['channel']].pop(0)

    # then we emit the new message
    channels_data[message_data['channel']].append(message_data)
    emit("receive message", message_data, broadcast=True)


@socketio.on('get channel messages')
def getChannelMessages(channel_name):
    data = [channel_name]

    if channels_data.get(channel_name) is None :
        # this if statement handles the creation of a new channel
        channels_data[channel_name] = []

    messages = channels_data.get(channel_name)
    data.append(messages)
    # we emit a tuple, the channel_name, and the messages
    emit("receive channel messages", data, broadcast=True)

@socketio.on('get channel list')
def getChannelList():
    channel_list = []
    for key, value in channels_data.items():
        channel_list.append(key)
    # emits the channel list
    emit("receive channel list", channel_list, broadcast=True)

@socketio.on('delete message')
def deleteMessage(message_data):

    # Take message_data and split it into variables
    channel = message_data['channel']
    timestamp = int(message_data['timestamp'])
    username = message_data['username']
    text = message_data['text']

    # iterate over list, since we don't have a database nor a message_id, we look for an exact match for all the fields
    for i in range(len(channels_data[channel])):
        message = channels_data[channel][i]
        if message['timestamp'] == timestamp and message['username'] == username and message['text'] == text:
            del channels_data[channel][i]
            break

    getChannelMessages(message_data['channel'])