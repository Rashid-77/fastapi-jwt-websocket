**This example project shows how to authenticate websocket with jwt token**

1. First of all create new websocket request in postman, and set header with name "secret".
2. Then import websocket-jwt-authentication-http.postman_collection.json from this project to the postman. Run it and you get response with jwt token. 
3. Copy this token from response and paste it into value field of "secret" of websocket's request.
4. Press "connect" button on the left of the websocket url.
5. If connection OK, you'll see "Connected to ws://127.0.0.1:8000/" in the response
6. Then go to tab messages of websocket request and send message. You'll receive echo back.

