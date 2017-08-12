from channels.routing import route

from one.consumers import ws_add, ws_message, ws_discard

channel_routing = [
    # route('http.request', "one.consumers.http_consumer")
    route('websocket.connect', ws_add),
    route('websocket.receive', ws_message),
    route('websocket.disconnect', ws_discard)
]
