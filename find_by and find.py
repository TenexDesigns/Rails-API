In Rails ActiveRecord, both find and find_by are methods used to retrieve records from the database. 
However, there are some differences between them:

find method:

Syntax: Model.find(id)
Usage: It is used to find a record by its primary key (id) value.
Behavior:
Raises an ActiveRecord::RecordNotFound exception if the record with the specified id is not found.
Returns a single record if found.
Can also accept an array of ids to retrieve multiple records.
Typically used when you expect the record to exist and want to handle the exception if it doesn't.
find_by method:

Syntax: Model.find_by(attribute: value)
Usage: It is used to find a record by specifying the attribute and its value.
Behavior:
Returns the first record that matches the specified attribute and value combination.
Returns nil if no matching record is found.
Can accept multiple attributes and values in the form of a hash.
Does not raise an exception if the record is not found.
Typically used when you want to retrieve a single record or handle the case when no record is found.
Heres an example to illustrate the difference:

# Using find
user = User.find(1)
# Returns the user with id 1, raises ActiveRecord::RecordNotFound if not found

# Using find_by
user = User.find_by(email: 'example@example.com')
# Returns the first user with email 'example@example.com' or nil if not found
In summary, find is used when you expect the record to exist and want to handle the exception
if it doesnt, while find_by is used to retrieve a single record by specifying attribute-value combinations 
and gracefully handle the case when no record is found.




























































..
