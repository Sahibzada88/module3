from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from llm import hacking_bot  # Import your chatbot function

app = Flask(__name__)
CORS(app)  # Enable CORS to allow Flutter app to communicate with the API

# Set up logging
logging.basicConfig(level=logging.INFO)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    question = data.get('question')
    user_id = data.get('user_id', '1')  # Default user ID if not provided

    logging.info("Received question from user_id %s: %s", user_id, question)
    
    response = hacking_bot(question, user_id)  # Call your chatbot function
    
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app
