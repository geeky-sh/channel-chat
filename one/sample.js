socket = new WebSocket('ws://' + window.location.host + '/chat/xxx/')

socket.onmessage = function(e) {
    console.log(e.data)
}

socket.onopen = function() {
    socket.send('Hello world for the first program')
}

if (socket.readyState == WebSocket.OPEN) socket.onopen()
