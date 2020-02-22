class Post:

    # Initializer / Instance Attributes
    def __init__(self, accountID, postID, items, location, starttime, duetime, contact, description, logistics, tags, requests):
        self.accountID = accountID
        self.postID = postID
        self.items = items
        self.location = location
        self.starttime = starttime
        self.duetime = duetime
        self.contact = contact
        self.description = description
        self.logistics = logistics
        self.tags = tags
        self.requests = requests

    # instance method
    def getAccountID(self):
        return self.accountID

    # instance method
    def getpostID(self):
        return self.postID

    # instance method
    def getitems(self):
        return self.items

    # instance method
    def getlocation(self):
        return self.location

    # instance method
    def getstarttime(self):
        return self.starttime

    # instance method
    def getduetime(self):
        return self.duetime

    # instance method
    def getcontact(self):
        return self.contact

    # instance method
    def getdescription(self):
        return self.description

    # instance method
    def getlogistics(self):
        return self.logistics

    # instance method
    def gettags(self):
        return self.tags

    # instance method
    def getrequests(self):
        return self.requests