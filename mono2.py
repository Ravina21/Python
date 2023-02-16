# libraries
import getpass
import pymongo
from random import randint
CONNECTION_STRING = getpass.getpass(
    prompt="Enter connection string available in networking tab of cosmos account: "
)
#print("Using " + CONNECTION_STRING + "to connect with MongoDB")
DATABASE = "Mongo"
COLLECTION = "Data"
FIELD = ("Employees","Mobile", "Address")

def create_database_unsharded_collection(client):
    """Create sample database with shared throughput if it doesn't exist and
    an unsharded collection
    """
    db = client[DATABASE]
    # Create database if it doesn't exist
    if DATABASE not in client.list_database_names():
        # Database with 400 RU throughput that can be shared across the
        # DB's collections
        db.command({"customAction": "CreateDatabase", "offerThroughput": 400})
        print("Created db {} with shared throughput".format(DATABASE))
    # Create collection if it doesn't exist
    if COLLECTION not in db.list_collection_names():
        # Creates a unsharded collection that uses the DBs shared throughput
        db.command(
            {
                "customAction": "CreateCollection",
                "collection": COLLECTION,
            }
        )
        print("Created collection {}".format(COLLECTION))
    return db[COLLECTION]

def insert_sample_document(collection):
    """Insert a sample document and return the contents of its _id field"""
    document_id = collection.insert_many([{
        FIELD: randint(50, 500),
        "Employee": {
      "Organization": "BFL",
      "Title": "Mrs.",
      "GivenName": "Jane",
      "MiddleName": "Lane",
      "FamilyName": "Doe",
      "Active": "true",},
      "Mobile": { "FreeFormNumber": "505.555.9999" },
      "Address": { "Address": "janedoe@example.com", "Line1": "123 Any Street",
        "City": "Any City",
        "CountrySubDivisionCode": "WA",
        "PostalCode": "01234"},
      "EmployeeType": "Regular",
      "Position": "Manager",
      "Id": "ABC123"}
         ]).inserted_id
    print("Inserted document with _id {}".format(document_id))
    return document_id
    
def main():
    client = pymongo.MongoClient(CONNECTION_STRING)
    try:
        client.server_info()  # validate connection string
    except pymongo.errors.ServerSelectionTimeoutError:
        raise TimeoutError(
            "Invalid API for MongoDB connection string \
                or timed out when attempting to connect"
        )
    collection = create_database_unsharded_collection(client)
    document_id = insert_sample_document(collection)
if __name__ == "__main__":
    main()
