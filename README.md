# Policy-Enforcer

A really simple policy enforcer, designed first for the Ceilometer API.

## How it works
The request are send to the policy enforcer, instead of the API.

Then, the PE will submit the request to a list of policies, which will decide to let (or not) the request to be processed.

If the policies accept, the request will be send, and the response return to the sender.
If not, a predefined string is returned as a response.

The policies will also analyze the response, for internal use.

## Use
Just launch the `policy_enforcer.py`

## Add new policies
First, you need to subclass the BasePolicy class in the `policy/base_policy.py` file.

Then, add a constructor in the `self.policy_collection` in `policy_enforcer.py` (check the __init__ function).

## TODO
* Stream the response. At the moment, receive the whole response, then send it, but can cause problem for really big responses.
