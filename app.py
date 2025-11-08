# jarvis/app.py
from flask import Flask, render_template, request, jsonify
from jarvis import process_text_query
from dotenv import load_dotenv
import os

# Load environment variables from a .env file 
load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    """Serves the main HTML template."""
   
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    """
    Endpoint for receiving user queries (text or transcript) and returning a reply.
    """
    try:
        data = request.json or {}
        q = data.get('query', '').strip()
        
        if not q:
            return jsonify(reply="Please provide a query.")
        
        
        reply = process_text_query(q)
        
       
        return jsonify(reply=reply)

    except Exception as e:
        app.logger.error(f"Error processing /ask request: {e}")
        return jsonify(reply="Error: An internal server error occurred."), 500

if __name__ == '__main__':
    # Flask runs on http://127.0.0.1:5000 by default
    port = int(os.environ.get("PORT", 5000))

    app.run(debug=True, port=port)
