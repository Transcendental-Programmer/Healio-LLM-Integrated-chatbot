from flask import Flask, request, jsonify, render_template
from src.chatbot import chatbot

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    if 'query' not in data:
        return jsonify({'error': 'Query is required'}), 400
    
    query = data['query']
    response = chatbot(query)
    
    return jsonify({'response': response})

@app.route('/hospital-rag-agent', methods=['POST'])
def hospital_rag_agent():
    data = request.json
    if 'text' not in data:
        return jsonify({'error': 'Text is required'}), 400
    
    query = data['text']
    response = chatbot(query)
    
    return jsonify({'output': response})

if __name__ == '__main__':
    app.run(debug=True, port=8000)