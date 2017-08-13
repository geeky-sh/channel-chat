from channels.routing import route, include

from one.consumers import ws_add, ws_receive, ws_discard, msg_consumer

chat_routing = [
    route('websocket.connect', ws_add, path=r"^/(?P<room_name>[a-zA-Z0-9_]+)/$"),
    route('websocket.receive', ws_receive, path=r"^/(?P<room_name>[a-zA-Z0-9_]+)/$"),
    route('websocket.disconnect', ws_discard, path=r"^/(?P<room_name>[a-zA-Z0-9_]+)/$"),
]
channel_routing = [
    include(chat_routing, path="^/chat"),
    route('chat-messages', msg_consumer)
    # route('http.request', "one.consumers.http_consumer")
]
