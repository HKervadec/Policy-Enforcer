# Policy-Enforcer

A really simple policy enforcer, designed first for the Ceilometer API.

## How it works
The request are send to the policy enforcer, instead of the API.

Then, the PE will submit the request to a list of policies, which will decide to let (or not) the request to be processed.

If the policies accept, the request will be send, and the response return to the client.
If not, an error message will be generated and return to the client.

The policies will also analyze the response, for internal use.

## Replacing the API endpoints
So far, it seems to be working.

### Modify public endpoint
Delete the current endpoint
```
keystone endpoint-list
keystone endpoint-delete <endpoint_id>

keystone service-list
```

In a json file
```
{
    "endpoint": 
        {
            "enabled": true,
            "interface": "<public|admin|internal>",
            "region": "RegionOne",
            "service_id": "<ceilometer_service_id>",
            "url": "<public_url|admin_url|internal_url>"
        }
}
```
Basically, the admin_url and the internal_url would be the same as before, only the public must change.

Then, for interface being public, admin, internal:
```
curl -X POST \
-H "X-Auth-Token: <token_id>" \
-H 'Content-Type: application/json' -d @<filename> \
http://<keystone_url>/v3/endpoints
```


## Use
Just launch the `policy_enforcer.py`
`./policy_enforcer.py -h` for help.

## Add new policies
First, you need to subclass the BasePolicy class in the `policy/base_policy.py` file.

Then, add a constructor in the `self.policy_collection` in `policy_enforcer.py` (check the __init__ function).

## TODO
* Stream the response. At the moment, receive the whole response, then send it, but can cause problem for really big responses.
