from pymongo import MongoClient




MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)

def connexioBDD():

    try:
        # start example code here
        # end example code here
        client.admin.command("ping")
        print("Connected successfully")
        db = client["acces_portes"]
        return db
        
    except Exception as e:
        raise Exception(
            "The following error occurred: ", e)
