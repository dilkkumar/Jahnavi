from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# MongoDB configuration
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
DB_NAME = 'portfolio_db'

# Initialize MongoDB client
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
contacts_collection = db['contacts']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    try:
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # Validate form data
        if not all([name, email, subject, message]):
            return jsonify({'success': False, 'message': 'All fields are required'})
        
        # Create contact document
        contact = {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message,
            'date': datetime.utcnow(),
            'read': False
        }
        
        # Insert into MongoDB
        contacts_collection.insert_one(contact)
        
        return jsonify({'success': True, 'message': 'Message sent successfully!'})
    
    except Exception as e:
        print(f"Error submitting form: {e}")
        return jsonify({'success': False, 'message': 'An error occurred. Please try again.'})

if __name__ == '__main__':
    app.run(debug=True)