import os

MONGO_URI = "mongodb://localhost:27017/hospital_db"
DB_NAME = "hospital_db"
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')