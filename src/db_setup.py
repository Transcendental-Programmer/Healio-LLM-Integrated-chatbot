import pandas as pd
from pymongo import MongoClient
import os
from config import MONGO_URI, DB_NAME, DATA_DIR

def clear_collection(collection_name):
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[collection_name]
    result = collection.delete_many({})
    print(f"Cleared {result.deleted_count} documents from {collection_name}")

def import_csv_to_mongodb(csv_file, collection_name, key_field):
    df = pd.read_csv(os.path.join(DATA_DIR, csv_file))
    data = df.to_dict('records')
    
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[collection_name]
    
    clear_collection(collection_name)
    
    for record in data:
        collection.update_one(
            {key_field: record[key_field]},
            {"$set": record},
            upsert=True
        )
    
    print(f"Imported/Updated {len(data)} records in {collection_name}")

def create_indexes():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    
    db.hospitals.create_index("hospital_id")
    db.patients.create_index("patient_id")
    db.physicians.create_index("physician_id")
    db.reviews.create_index("review_id")
    db.visits.create_index("visit_id")
    
    print("Indexes created successfully")

if __name__ == "__main__":
    import_csv_to_mongodb('hospitals.csv', 'hospitals', 'hospital_id')
    import_csv_to_mongodb('patients.csv', 'patients', 'patient_id')
    import_csv_to_mongodb('payers.csv', 'payers', 'payer_id')
    import_csv_to_mongodb('physicians.csv', 'physicians', 'physician_id')
    import_csv_to_mongodb('reviews.csv', 'reviews', 'review_id')
    import_csv_to_mongodb('visits.csv', 'visits', 'visit_id')
    create_indexes()