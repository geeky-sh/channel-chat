from django.http import JsonResponse
from channels.handler import AsgiHandler
from channels import Group
from channels.sessions import channel_session
from urlparse import parse_qs
import random


def http_consumer(message):
    resp = JsonResponse({'hello': 'world'})

    for chunk in AsgiHandler.encode_response(resp):
        message.reply_channel.send(chunk)


# Connected to websocket.connect
def ws_add(message):
    # Accept the connection
    message.reply_channel.send({"accept": True})
    # Add to the chat group
    Group("chat").add(message.reply_channel)


# Connected to websocket.receive
def ws_message(message):
    num = random.randint(1, 10)
    Group("chat").send({
        "text": "The random number is %s , msg %s" % (num, message.content['text'],)
    })


# Connected to websocket.disconnect
def ws_discard(message):
    Group("chat").discard(message.reply_channel)

# @channel_session
# def ws_add(message, room):
#     import ipdb; ipdb.set_trace();
#     # to accept the incoming connection
#     message.reply_channel.send({'accept': True})

#     params = parse_qs(message.content['query_string'])
#     if 'name' in params:
#         message.channel_session['name'] = params['name']

#         Group('chat-%s' % (room,)).add(message.reply_channel)
#     else:
#         message.reply_channel({'close': True})


# @channel_session
# def ws_receive(message, room):
#     import ipdb; ipdb.set_trace();
#     username = message.channel_session['name']
#     Group('chat-%s' % (room,)).send({
#         "text": "hello people, this is my msg %s" % (message.content['text'],),
#         'username': username
#     })


# @channel_session
# def ws_discard(message, room):
#     username = message.channel_session['name']
#     print(username)
#     Group('chat-%s' % (room,)).discard(message.reply_channel)
