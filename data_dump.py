import pymongo
import pandas as pd
import json 

# Provide the mongodb localhost url to connect python to mongodb.
from sensor.config import mongo_client

DATA_FILE_PATH="/config/workspace/aps_failure_training_set1.csv"
# Database Name
dataBase = "APS_Failure_Detection"
# Collection  Name
collection = "sensor"
if __name__=="__main__":
    df=pd.read_csv(DATA_FILE_PATH)
    print(f"Rows and columns: {df.shape}")
    # reseting the index
    df.reset_index(drop=True,inplace=True)
    #Convert dataframe to json so that we can dump these record in mongo db
    json_record = list(json.loads(df.T.to_json()).values())# this is the required format
    #print(json_record[0])

    # insert converted json record to modgoDB
    mongo_client[dataBase][collection].insert_many(json_record)

