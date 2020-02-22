class AccountID:

    # Initializer / Instance Attributes
    def __init__(self, accountID, name, notifications, filters, posts, requests):
        self.accountID = accountID
        self.name = name
        self.notifications = notifications
        self.filters = filters
        self.posts = posts
        self.requests = requests

    # instance method
    def getAccountID(self):
        return self.accountID

    # instance method
    def getName(self):
        return self.name

    # instance method
    def getnotifications(self):
        return self.notification

    # instance method
    def getfilters(self):
        return self.notifications

    # instance method
    def getposts(self):
        return self.posts

    # instance method
    def getrequests(self):
        return self.requests

    def get_db_notifications(self):
        return ','.join(self.notifications)

    def get_db_filters(self):
        return ','.join(self.filters)

    def get_db_posts(self):
        return ','.join(self.posts)

    def get_db_requests(self):
        return ','.join(self.requests)