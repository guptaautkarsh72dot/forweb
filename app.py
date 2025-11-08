from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

# Sample data storage (in production, use a database)
data_store = []

@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    """Get all data"""
    return jsonify({
        'success': True,
        'data': data_store
    })

@app.route('/api/data', methods=['POST'])
def add_data():
    """Add new data"""
    try:
        data = request.get_json()
        
        # Backend logic: Process and validate the data
        if not data or 'message' not in data:
            return jsonify({
                'success': False,
                'error': 'Message is required'
            }), 400
        
        # Process the data (example: capitalize first letter)
        processed_message = data['message'].strip()
        if processed_message:
            processed_message = processed_message[0].upper() + processed_message[1:] if len(processed_message) > 1 else processed_message.upper()
        
        # Store the processed data
        new_item = {
            'id': len(data_store) + 1,
            'message': processed_message,
            'timestamp': data.get('timestamp', '')
        }
        data_store.append(new_item)
        
        return jsonify({
            'success': True,
            'data': new_item
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/data/<int:item_id>', methods=['DELETE'])
def delete_data(item_id):
    """Delete data by ID"""
    global data_store
    original_length = len(data_store)
    data_store = [item for item in data_store if item['id'] != item_id]
    
    if len(data_store) < original_length:
        return jsonify({
            'success': True,
            'message': 'Item deleted successfully'
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Item not found'
        }), 404

@app.route('/api/process', methods=['POST'])
def process_data():
    """Example endpoint for processing data on the backend"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'success': False,
                'error': 'Text is required'
            }), 400
        
        text = data['text']
        
        # Backend logic: Process the text
        word_count = len(text.split())
        char_count = len(text)
        reversed_text = text[::-1]
        uppercase_text = text.upper()
        
        return jsonify({
            'success': True,
            'result': {
                'original': text,
                'word_count': word_count,
                'char_count': char_count,
                'reversed': reversed_text,
                'uppercase': uppercase_text
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("Starting Flask server...")
    print("Backend will be available at: http://localhost:5000")
    print("Frontend will be available at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

