import os
import sys
import json
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

import certifi
ca=certifi.where()

import pandas as pd
import numpy as np
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def csv_to_json_convertor(self,file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records=list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    
    def insert_data_mongodb(self,records,database,collection):
        try:
            self.database=database
            self.collection=collection
            self.records=records

            # Encode the username and password using quote_plus
            username = "Sanyamjhuria"
            password = "Sanyam@123"  # Use your actual password
            encoded_username = quote_plus(username)
            encoded_password = quote_plus(password)

            # Construct the MongoDB URI with encoded username and password
            uri = f"mongodb+srv://{encoded_username}:{encoded_password}@cluster0.3wnmwv1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

            # Use the encoded URI
            self.mongo_client = pymongo.MongoClient(uri)
            self.database=self.mongo_client[self.database]
            self.collection=self.database[self.collection]
            self.collection.insert_many(self.records)
            return (len(self.records))
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

if __name__== "__main__":
    FILE_PATH=r"Network_Data\phisingData.csv"
    DATABASE="SANYAMAI"
    Collection="NetworkData"
    networkobj=NetworkDataExtract()
    records=networkobj.csv_to_json_convertor(file_path=FILE_PATH)
    #print(records)
    no_of_records=networkobj.insert_data_mongodb(records,DATABASE,Collection)
    print(no_of_records)