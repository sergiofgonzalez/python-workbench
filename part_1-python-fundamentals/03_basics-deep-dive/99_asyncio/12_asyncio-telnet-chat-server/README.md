# An async chat server written in Python
> a port of the Node.js chat server using asyncio streams


## Running the app

To run the server on the default port type:

```bash
uv run server.py
```

You can connect to the chat using `telnet`:

```bash
$ telnet 127.0.0.1 8888
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
Congratulations! You've successfully joined the chat server.
Your id is: '127.0.0.1:36832'.
There are 1 client(s) connected to this server.
```

## Description

+ Caps the number of clients to 50
+ Keeps a list of clients in a dict, whose key is the client_id, and value is the client socket so that you can read and write to it.
+ Keeps a list of subscriptions whose key is the client_id, and value is the subscription function.


### Events: join

A join event receives the client_id and the socket associated to that client.

When a join event is triggered, the new client is added to the clients dict.

And the following subscription function is added to the dictionary of subscriptions:
+ A function that receives the sender client_id, and the message to send. The function sends the received message to all other clients (that is, the message is not sent to the one that originated the message for obvious reasons).

+ The client_id is registered for the broadcast event.

+ A message is sent to the recently connected client:

```
Congratulations! You've successfully joined the chat server.
Your id is: ${id}
There are N clients connected to this server.
```

where N is the current number of clients.

Additionally, a message is broadcasted (to all clients except to the one that joined): `A new client has connected to the chat: id = {client_id}`.


### Events: broadcast

A broadcast event receives the sender client_id and a message. The message is sent to all clients except to the one that originated the message. The subscription function is used to be associated to this event.

### Events: leave

A leave event receives the client_id.

When triggered, the broadcast subscription is removed for that client, as well as the entry from the subscriptions and clients dict.

Finally, a broadcast message is emitted: `$id has left the chat`.

### Events: shutdown

A shutdown event receives no arguments.

When triggered, a broadcast message is sent to all the connected clients: `The chat has been shut down`.

All listeners of broadcast, subscriptions, and clients are removed. A message is also printed in the server so that ops now that the shutdown event has been received.


### Main program

A server is created with a callback that receives the client socket.

the client_id is calculated as: `client.remoteAddress:client.port`

Then a message is printed: A new connection has been received.

Right after that, a join event is triggered.

Then, a callback for the socket.data event is registered. This event is triggered when there is some inbound data transfer in the socket.

In the callback, the message is read, if it happens to be the string "SHUTDOWN\r\n" (as sent by telnet) the shutdown event is triggered, otherwise, the reveived message is broadcasted.

Then, a callback for the socket.close event is registered, triggering the leave event.

Also, a callback for the socket.error event is registered, raising a custom error.

Then, the server is established on port 8888, and the message: `Waiting for incoming connections on port 8888` is triggered.
