import pymongo
import pandas as pd
import json
from dataclasses import dataclass 
import os

class EnvironmentVariable:
    mongo_db_url:str = os.getenv("MONGO_DB_URL")
    #aws_access_key_id:str = os.getenv("AWS_ACCESS_KEY_ID")
    #aws_access_secret_key:str = os.getenv("AWS_SECRET_ACCESS_KEY")



env_var = EnvironmentVariable()
mongo_client = pymongo.MongoClient(env_var.mongo_db_url)
TARGET_COLUMN = "class"
# parameter for xgbooost
params = {
        'min_child_weight': [1, 5, 10],
        'gamma': [0.5, 1, 1.5, 2, 5],
        'subsample': [0.6, 0.8, 1.0],
        'colsample_bytree': [0.6, 0.8, 1.0],
        'max_depth': [3, 4, 5]
        }