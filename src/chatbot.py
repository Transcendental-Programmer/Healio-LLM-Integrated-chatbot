from src.rag_system import rag_system

def chatbot(query):
    # Find similar documents
    similar_docs = rag_system.find_similar_documents(query)
    context = "\n".join([doc['text'] for doc in similar_docs])

    # Process the query
    mongodb_query = rag_system.process_query(query)
    
    try:
        # Execute the generated query
        query_results = rag_system.execute_query(mongodb_query)
        
        if not query_results:
            return "I'm sorry, I couldn't find any information related to your query. Could you please rephrase or provide more details?"
        
        # Generate a human-readable response based on the query results and context
        context += "\n" + str(query_results)
        final_response = rag_system.generate_response(query, context)
        return final_response
    except Exception as e:
        print(f"Error in chatbot: {str(e)}")
        return "I'm sorry, I encountered an error while trying to retrieve the information. Could you please try rephrasing your question?"