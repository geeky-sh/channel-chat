from django.http import JsonResponse
from channels.handler import AsgiHandler
from channels import Group, Channel
from channels.sessions import channel_session
from channels.auth import channel_session_user_from_http, channel_session_user
from urlparse import parse_qs
import random
import json
from .models import ChatMessage


def http_consumer(message):
    resp = JsonResponse({'hello': 'world'})

    for chunk in AsgiHandler.encode_response(resp):
        message.reply_channel.send(chunk)


def msg_consumer(message):
    name = message['name']
    room = message['room']
    message = message['text']

    ChatMessage.objects.create(name=name, room=room, message=message)

    Group('chat-%s' % (room,)).send({
        'text': json.dumps({
            'text': message,
            'name': name
        })
    })


# Connected to websocket.connect
# def ws_add(message):
#     # Accept the connection
#     message.reply_channel.send({"accept": True})
#     # Add to the chat group
#     Group("chat").add(message.reply_channel)


# # Connected to websocket.receive
# def ws_message(message):
#     num = random.randint(1, 10)
#     Group("chat").send({
#         "text": "The random number is %s , msg %s" % (num, message.content['text'],)
#     })


# # Connected to websocket.disconnect
# def ws_discard(message):
#     Group("chat").discard(message.reply_channel)

@channel_session_user_from_http
def ws_add(message, room_name):
    # to accept the incoming connection
    message.reply_channel.send({'accept': True})

    params = parse_qs(message.content['query_string'])
    if b'name' in params:
        message.channel_session['name'] = params[b"name"][0].decode("utf8")

        Group('chat-%s' % (room_name,)).add(message.reply_channel)
    else:
        message.reply_channel({'close': True})


@channel_session_user
def ws_receive(message, room_name):
    print room_name
    username = message.channel_session['name']
    Channel('chat-messages').send({
        'room': room_name,
        'text': message['text'],
        'name': message.channel_session['name']
    })


@channel_session_user
def ws_discard(message, room_name):
    username = message.channel_session['name']
    print(username)
    Group('chat-%s' % (room_name,)).discard(message.reply_channel)
