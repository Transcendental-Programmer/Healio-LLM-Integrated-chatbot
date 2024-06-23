from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
import numpy as np
from config import MONGO_URI, DB_NAME

def create_vector_store():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    
    vector_store = db['vector_store']
    vector_store.drop()  
    
    for collection_name in ['hospitals', 'patients', 'physicians', 'reviews', 'visits']:
        collection = db[collection_name]
        for doc in collection.find():
            text = ' '.join([f"{k}: {v}" for k, v in doc.items() if k != '_id'])
            embedding = model.encode(text).tolist()
            
            vector_store.insert_one({
                'text': text,
                'embedding': embedding,
                'collection': collection_name
            })
    
    print("Vector store created successfully")

if __name__ == "__main__":
    create_vector_store()