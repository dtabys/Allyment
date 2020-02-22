
from twilio.rest import Client

class notification:

    def notify(accountID, auth_token):
            # put your own credentials here
            account_sid = accountID
            auth_token = "9a22883785fdb5b26fc4406d43677cc9"
            client = Client(account_sid, auth_token)
            client.messages.create(
            to="+14805439520",
            from_="+19737185004",
            body="Testing"