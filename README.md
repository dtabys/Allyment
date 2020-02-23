# Allyment
-Allyment is an interactive web based application where we aim to connect people around the world who wish to donate surplus food to non-profit organizations.
Account.py:
-	Constructor: initialize class variables
-	getAccountId: Returns Account Id.
-	getName: Returns Name.
-	getnotifications: Returns notifications
-	getfilters: Returns filters
-	getrequests: Returns requests
-	get_db_notifications: Returns a String of all notifications from database.
-	get_db_posts; Returns a String of all posts from database.
-	get_db_requests: Returns a String of all requests from database.
-	get_db_array: Returns an array of String which includes name, password, notification, filter, posts, requests.


Item.py
-	Constructor: initialize class variables
-	getAccountId: Returns Account Id.
-	getname: Returns Name.
-	getdescription: Returns description.
-	Gettags: returns tags.
-	Getquantity: returns quantity.
-	getItemId: returns ItemId.
-	Get_db_tags: Returns a String of all tags from database.


Posts.py
-	Constructor: Initialize class variables.
-	getAccountId: Returns Account Id.
-	getpostId: Returns Post id.
-	getItems: Returns Items.
-	getLocation: Returns Location.
-	getStartTime: Returns Start time.
-	getEndTime: Returns End Time.
-	getContacts: Returns Contact.
-	getDescription: Returns Description.
-	getLogistics: Returns Logistics.
-	getTags: Returns Tags.
-	getRequests: Returns Requests.
-	getName: Returns Name.
-	get_db_location: Returns a String of all Locations.
-	get_db_Items: Returns a String of all Items.
-	get_db_logistcis; Returns a String of all Logistics.
-	get_db_tags: Returns a String of all Tags.
-	get_db_requests: Returns a String of all Requests.
-	get_db_array: Returns a String of all class variables.


Request.py:
-	Constructor: Initializes class variables.
-	getAccountId: Returns Account Id
-	getRequestId: Returns Request id.
-	getPostId: Returns PostId.
-	getItems; Returns Items.
-	getQuantity: Returns Quantity.
-	Get_db_items: Returns a String of all Items.


Notifiation.py
-	Constructor: initializes class variables.
-	Notify: Sends the client notification via text message.


Database.py
-	Hash_password: hashing the password
-	Salt_key: prevents similar hashing of 2 same passwords.
-	Create table: Creates a table.
-	Check_login: checks login credentials.
-	Register_account: registers a new account into the database with default values.
-	Get_account: Returns account information.
-	Add_post: Returns the last location in post array.
-	Get_post: Returns the post information.
-	add_item: returns the last location in the item array.
-	Get_item: Returns the item information.
-	Add_request: Returns the last location of request array.
-	Get_request: Returns the request information.
-	Init_tables: creates tables of accounts, posts, items, requests.


Deploy.sh
-	It is used to deploy the application to the customer.
