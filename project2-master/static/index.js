document.addEventListener('DOMContentLoaded', () => {

    if (localStorage.getItem('username') === null) {
        // prompts user to enter a username if there isn't one in localStorage
        var temp = prompt('Please enter a username');
        localStorage.setItem('username', temp);
    }

    // Greeting with username
    document.querySelector('#username_display').innerHTML = localStorage.getItem('username');

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure
    socket.on('connect', () => {

        loadChannel();

        // Execute a function when the user releases a key on the keyboard
        document.getElementById('message_text').addEventListener('keyup', function(event) {
            //this eventlistener from https://www.w3schools.com/howto/howto_js_trigger_button_enter.asp
            // Cancel the default action, if needed
            event.preventDefault();
            // Number 13 is the "Enter" key on the keyboard
            if (event.keyCode === 13) {
                // Trigger the button element with a click
                document.getElementById('send_message').click();
            }
        });

        document.querySelector('#send_message').onclick = () => {
            // We emit the message and all it's data
            channel = localStorage.getItem('selected_channel');
            timestamp = (new Date()).valueOf();
            username = localStorage.getItem('username');
            text = document.querySelector('#message_text').value;
            message_data = {
                'channel': channel,
                'timestamp': timestamp,
                'username': username,
                'text': text
            };

            socket.emit('send message', message_data);

            document.querySelector('#message_text').value = ''; // Clears the input box
        };

        // Execute a function when the user releases a key on the keyboard
        document.getElementById('channel_name_input').addEventListener("keyup", function(event) {
            //this eventlistener from https://www.w3schools.com/howto/howto_js_trigger_button_enter.asp
            // Cancel the default action, if needed
            event.preventDefault();
            // Number 13 is the "Enter" key on the keyboard
            if (event.keyCode === 13) {
                // Trigger the button element with a click
                document.getElementById('go_to_channel').click();
            }
        });

        document.querySelector('#go_to_channel').onclick = () => {
            // If the channel to be navigated to isn't the current channel, then load it
            if (document.querySelector('#channel_name_input').value !== localStorage.getItem('selected_channel')) {
                localStorage.setItem('selected_channel', document.querySelector('#channel_name_input').value);
                loadChannel();
                document.querySelector('#channel_name_input').value = '';
            }
        };
    });



    socket.on('receive message', message => {
        if (message.channel === localStorage.getItem('selected_channel')) {
            // Display received messages
            const li = document.createElement('li');
            display_timestamp = (new Date(message.timestamp)).toLocaleString('en-US');
            if (localStorage.getItem('username') === message.username) {
                utc_date = (new Date(message.timestamp)).valueOf().toString();
                li.innerHTML = display_timestamp + ' <br/><span class="username_message">' + message.username + '</span>:: ' + message.text + "<br/>"
                                    + '<button type="button" id="delete_message" onClick="deleteMessage('+  utc_date + ',\''+ message.text + '\')">Delete</button><br/><br/>';
            } else {
                li.innerHTML = display_timestamp + ' <br/><span class="username_message">' + message.username + '</span>:: ' + message.text + "<br/><br/>";
            }
            document.querySelector('#messages').append(li);
        }
    });

    socket.on('receive channel messages', data => {
        channel_name = data[0];
        messages = data[1];
        if (channel_name === localStorage.getItem('selected_channel')) {
            // Clear all previous messages
            while (document.querySelector('#messages').firstChild) {
                document.querySelector('#messages').removeChild(document.querySelector('#messages').firstChild);
            }

            // Add messages to the UI
            for (i in messages) {
                const li = document.createElement('li');
                display_timestamp = (new Date(messages[i].timestamp)).toLocaleString('en-US');
                if (localStorage.getItem('username') === messages[i].username) {
                    utc_date = (new Date(messages[i].timestamp)).valueOf().toString();
                    li.innerHTML = display_timestamp + ' <br/><span class="username_message">' + messages[i].username + '</span>:: ' + messages[i].text + "<br/>"
                                        + '<button type="button" id="delete_message" onClick="deleteMessage('+  utc_date + ',\''+ messages[i].text + '\')">Delete</button><br/><br/>';
                } else {
                    li.innerHTML = display_timestamp + ' <br/><span class="username_message">' + messages[i].username + '</span>:: ' + messages[i].text + "<br/><br/>";
                }
                document.querySelector('#messages').append(li);
            }
        }
    });

    socket.on('receive channel list', channel_list => {

        localStorage.setItem('channel_list', channel_list);

        // Clear all previous channel list
        while (document.querySelector('#channels').firstChild) {
            document.querySelector('#channels').removeChild(document.querySelector('#channels').firstChild);
        }

        // Add channels to the UI
        for (i in channel_list) {
            const bu = document.createElement('button');
            bu.id = 'channel_chooser';
            bu.textContent = channel_list[i];
            bu.value = channel_list[i];

            document.querySelector('#channels').append(bu);
        }

        function changeChannel() {
            if (this.value !== localStorage.getItem('selected_channel')) {
                // If channel is different, load the channel
                localStorage.setItem('selected_channel', this.value);
                loadChannel();
            }
        }

        document.querySelectorAll('#channel_chooser').forEach(button => {
            button.onclick = changeChannel;
        });
    });

    function loadChannel() {
        if (localStorage.getItem('selected_channel') === null) {
            localStorage.setItem('selected_channel', 'general'); // Default channel if e.g. loading page for the very first time
        }

        document.querySelector('#channel_display').innerHTML = localStorage.getItem('selected_channel');

        socket.emit('get channel messages', localStorage.getItem('selected_channel'));
        socket.emit('get channel list');
    }
});

function deleteMessage(timestamp, message_text) {

    // We emit the message and all it's data
    channel = localStorage.getItem('selected_channel');
    timestamp = (new Date(timestamp)).valueOf().toString();
    username = localStorage.getItem('username');
    text = message_text;
    message_data = {
        'channel': channel,
        'timestamp': timestamp,
        'username': username,
        'text': text
    };

    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    socket.emit('delete message', message_data);
}
