class Item:

    def __init__(self, accountID, postID, name, description, tags, quantity, itemID):
        self.accountID = accountID
        self.postID = postID
        self.name = name
        self.description = description
        self.tags = tags
        self.quantity = quantity
        self.itemID = itemID

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

    # instance method
    def getitemID(self):
        return self.itemID

    def get_db_tags(self):
        return ','.join(self.tags)

    def get_db_array(self):
        return [self.accountID, self.postID, self.name, self.description, self.get_db_tags(), self.quantity]
