from pymongo import MongoClient
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import json
from src.config import MONGO_URI, DB_NAME
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class RAGSystem:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DB_NAME]
        self.model = GPT2LMHeadModel.from_pretrained('gpt2')
        self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')
 
        if self.db['vector_store'].count_documents({}) == 0:
            print("Vector store is empty. Please run vector_store.py to populate it.")

        self.db_schema = {
            "hospitals": ["hospital_id", "hospital_name", "hospital_state"],
            "patients": ["patient_id", "patient_blood_type", "patient_dob", "patient_name", "patient_sex"],
            "payers": ["payer_id", "payer_name"],
            "physicians": ["physician_id", "medical_school", "physician_dob", "physician_grad_year", "physician_name", "salary"],
            "reviews": ["review_id", "hospital_name", "patient_name", "physician_name", "review", "visit_id"],
            "visits": ["visit_id", "admission_type", "billing_amount", "chief_complaint", "date_of_admission", "discharge_date", "hospital_id", "patient_id", "payer_id", "physician_id", "primary_diagnosis", "room_number", "test_results", "treatment_description", "visit_status"]
        }

    def generate_text(self, prompt, max_length=1000):
        inputs = self.tokenizer(prompt, return_tensors="pt", padding=True, truncation=True, max_length=1024)
        attention_mask = inputs['attention_mask']
        
        output = self.model.generate(
            input_ids=inputs['input_ids'],
            attention_mask=attention_mask,
            max_length=max_length,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            temperature=0.7,
            top_k=50,
            top_p=0.95,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id
        )
        return self.tokenizer.decode(output[0], skip_special_tokens=True)

    def process_query(self, user_query):
        schema_info = json.dumps(self.db_schema, indent=2)
        prompt = f"""
        User query: {user_query}

        Database schema:
        {schema_info}

        Task: Analyze the user query and generate a MongoDB query to retrieve the necessary information.
        Your response should be a valid MongoDB query in Python dictionary format.
        Start your response with 'MongoDB query:' followed by the dictionary on a new line.

        For example:
        MongoDB query:
        {{
            "field_name": "value"
        }}

        Now, generate the MongoDB query:
        """

        response = self.generate_text(prompt)
        return response
    
    def execute_query(self, query):
        try:
            # Remove any leading/trailing whitespace and newlines
            query = query.strip()
            
            # If the query starts with a curly brace, assume it's a valid dictionary
            if query.startswith('{'):
                query_dict = eval(query)
            else:
                # If not, try to extract a dictionary from the generated text
                start = query.find('{')
                end = query.rfind('}')
                if start != -1 and end != -1:
                    query_dict = eval(query[start:end+1])
                else:
                    raise ValueError("No valid dictionary found in the query")

            # Determine the collection to query
            collection_name = next((col for col in self.db_schema.keys() if col in query.lower()), 'hospitals')
            
            # Execute the MongoDB query
            result = list(self.db[collection_name].find(query_dict).limit(10))
            return result
        except Exception as e:
            print(f"Error executing MongoDB query: {str(e)}")
            print(f"Generated query: {query}")
            return []
    
    def generate_response(self, user_query, context):
        prompt = f"Context: {context}\n\nQuestion: {user_query}\n\nGenerate a human-readable response:"
        return self.generate_text(prompt, max_length=1000)

    def find_similar_documents(self, query, k=5):
        query_embedding = self.sentence_transformer.encode([query])[0]
        vector_store = list(self.db['vector_store'].find())
        
        if not vector_store:
            return []
        
        embeddings = [doc['embedding'] for doc in vector_store]
        similarities = cosine_similarity([query_embedding], embeddings)[0]
        
        top_k_indices = similarities.argsort()[-k:][::-1]
        
        return [vector_store[i] for i in top_k_indices]

rag_system = RAGSystem()