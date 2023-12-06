**This example project shows how to authenticate websocket with jwt token**

Build project and run it.

Then start postman (tested on Postman for Linux version 10.20.10).

1. First of all create new websocket request (not http) in postman, set link "ws://127.0.0.1:8000/" and set new header with name "secret".
2. Then import "websocket-jwt-authentication-http.postman_collection.json" from this project to the postman. 
3. Send this http requst and you'll get response with jwt token. 
4. Copy this token from response and paste it into value field of "secret" of websocket's request.
5. Press "connect" button on the left of the websocket url.
6. If connection OK, you'll see "Connected to ws://127.0.0.1:8000/" in the response
7. Then go to tab messages of websocket request write something and send message. You'll receive echo back.
8. If connection can't established then token expired, repeat 3,4 and 5 steps

