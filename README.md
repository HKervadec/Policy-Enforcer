# Policy-Enforcer

A really simple policy enforcer, designed first for the Ceilometer API.

It is just a middleware, receiving the requests in place of the API, then decide to send or not the request to the API.

## TODO
* Stream the response. At the moment, receive the whole response, then send it, but can cause problem for really big responses.
