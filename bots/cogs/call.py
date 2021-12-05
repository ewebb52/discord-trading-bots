import os
from twilio.rest import Client
import cogs.acc as a

def make_call(messageContent, author):
    # Your Account Sid and Auth Token from twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid = a.account_sid
    auth_token = a.auth_token
    client = Client(account_sid, auth_token)
    print("Placing phone call...")
    call = client.calls.create(
                            twiml='<Response><Say>Ahoy, World!</Say></Response>',
                            to='+XXXXXXXXXX',
                            from_='+XXXXXXXX'
                        )

    #print(call.sid)