class Request:

    # Initializer / Instance Attributes
    def __init__(self, accountID, requestID, postID, items, quantity):
        self.accountID = accountID
        self.requestID = requestID
        self.postID = postID
        self.items = items
        self.quantity = quantity

    # instance method
    def getAccountID(self):
        return self.accountID

    # instance method
    def getrequestID(self):
        return self.requestID

    # instance method
    def getpostID(self):
        return self.postID

    # instance method
    def getitems(self):
        return self.items

    # instance method
    def getquantity(self):
        return self.quantity

    def get_db_items(self):
        return ', '.split(self.items)
