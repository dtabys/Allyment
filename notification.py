
from twilio.rest import Client

class notification:
    def __init__(self, accountID, auth_token):
        self.accountID = accountID
        self.token = auth_token

    def notify(self, contact, msg):
            # put your own credentials here
            client = Client(self.accountID, self.token)
            client.messages.create(
            to=contact,
            from_="+19737185004",
            body=msg
            )
