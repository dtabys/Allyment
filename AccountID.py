class AccountID:

    # Initializer / Instance Attributes
    def __init__(self, accountID, name, notifications, filters, posts, requests):
        self.accountID = accountID
        self.name = name
        self.notifications = notifications
        self.filters = filters
        self.posts = posts
        self.requests = requests

    #instance method
    def getAccountID(self):
        return "The accountID is: ".format(self.accountID)

    # instance method
    def getName(self):
        return "The Name is: ".format(self.name)

    #instance method
    def getnotifications(self):
        return "The notifications are: ".format(self.notification)

    #instance method
    def getfilters(self):
        return "The filters are: ".format(self.notifications)

    #instance method
    def getfilters(self):
        return "The filters are: ".format(self.filters)

    #instance method
    def getposts(self):
        return "The posts are: ".format(self.posts)

    #instance method
    def getrequests(self):
        return "The requests are: ".format(self.requests)


