class Item:

    # Initializer / Instance Attributes
    def __init__(self, accountID, postID, name, description, tags, quantity):
        self.accountID = accountID
        self.postID = postID
        self.name = name
        self.description = description
        self.tags = tags
        self.quantity = quantity

    # instance method
    def getAccountID(self):
        return self.accountID

    # instance method
    def getpostID(self):
        return self.postID

    # instance method
    def getname(self):
        return self.name

    # instance method
    def getdescription(self):
        return self.description

    # instance method
    def gettags(self):
        return self.tags

    # instance method
    def getquantity(self):
        return self.quantity