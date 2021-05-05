 const roomName = JSON.parse(document.getElementById('room_name').textContent);
        const request_username = JSON.parse(document.getElementById('user_username').textContent);

        const chatSocket = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/chat/'
            + roomName
            + '/'
        );

        chatSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            
            document.querySelector('#chat-log').innerHTML += '<p class="ui">' + (data.request_username + ':' + data.message + '</p>' + '\n');
        };

        chatSocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };

        document.querySelector('#chat-message-input').focus();
        document.querySelector('#chat-message-input').onkeyup = function(e) {
            if (e.keyCode === 13) {  // enter, return
                document.querySelector('#chat-message-submit').click();
                // 
            }
        };

        document.querySelector('#chat-message-submit').onclick = function(e) {
            const messageInputDom = document.querySelector('#chat-message-input');
            const message = messageInputDom.value;
            chatSocket.send(JSON.stringify({
                'message': message,
                'request_username' : request_username,
                
            }));
            messageInputDom.value = '';
        };


        


