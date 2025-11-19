from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import requests
import os

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)  # Enable CORS for frontend requests

# OpenRouter API configuration
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '')
OPENROUTER_API_URL = 'https://openrouter.ai/api/v1/chat/completions'
MODEL = 'openai/gpt-oss-20b:free'

@app.route("/api/test", methods=["GET"])
def test():
    """Test endpoint to verify API is working"""
    return jsonify({
        'status': 'API is working!',
        'message': 'This is a test message from the Flask backend. If you see this, the API is connected properly.'
    })

@app.route("/api/generate_trip", methods=["POST"])
def generate():
    try:
        data = request.json
        print(f"Received data: {data}")  # Debug log
        
        # Validate required fields
        required_fields = ['destination', 'boarding', 'duration', 'people', 'budgetMin', 'budgetMax']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check if API key is set
        if not OPENROUTER_API_KEY:
            return jsonify({
                'error': 'OpenRouter API key not configured',
                'message': 'Please set OPENROUTER_API_KEY environment variable'
            }), 500
        
        # Construct the prompt
        prompt = f"""Act as a travel planner. Use these details:

Destination: {data['destination']}
Boarding Point: {data['boarding']}
Duration: {data['duration']} days
Number of People: {data['people']}
Budget: ₹{data['budgetMin']} to ₹{data['budgetMax']}

Please provide a comprehensive travel itinerary including:
1. Top attractions to visit
2. Places on the way (between boarding point and destination)
3. Daily plan for each day
4. Estimated cost breakdown
5. Travel tips and recommendations

Format your response Paragraph and bullet points, dont give tables and format in a clear, organized manner with sections for each category."""

        # Prepare the request to OpenRouter
        headers = {
            'Authorization': f'Bearer {OPENROUTER_API_KEY}',
            'Content-Type': 'application/json',
            'HTTP-Referer': request.headers.get('Referer', 'http://localhost:5000'),
            'X-Title': 'TrekzaWorld Travel Planner'
        }
        
        payload = {
            'model': MODEL,
            'messages': [
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'temperature': 0.7,
            'max_tokens': 2000,
            'extra_body': {
                'reasoning': {
                    'enabled': True
                }
            }
        }
        
        print(f"Sending request to OpenRouter with model: {MODEL}")  # Debug log
        
        # Make request to OpenRouter
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload, timeout=30)
        
        print(f"OpenRouter response status: {response.status_code}")  # Debug log
        
        if response.status_code != 200:
            error_text = response.text
            print(f"OpenRouter error: {error_text}")  # Debug log
            return jsonify({
                'error': 'Failed to generate itinerary',
                'status_code': response.status_code,
                'details': error_text
            }), response.status_code
        
        result = response.json()
        print(f"OpenRouter response keys: {result.keys() if isinstance(result, dict) else 'Not a dict'}")  # Debug log
        
        # Extract the message content
        if 'choices' in result and len(result['choices']) > 0:
            message = result['choices'][0]['message']['content']
            print(f"Message length: {len(message) if message else 0}")  # Debug log
            
            if not message or len(message.strip()) == 0:
                return jsonify({
                    'error': 'Empty response from AI',
                    'raw_response': result
                }), 500
            
            return jsonify({'message': message})
        else:
            print(f"Unexpected response structure: {result}")  # Debug log
            return jsonify({
                'error': 'Unexpected response format from AI',
                'details': result
            }), 500
            
    except requests.exceptions.RequestException as e:
        print(f"Request exception: {str(e)}")  # Debug log
        return jsonify({
            'error': 'Failed to connect to AI service',
            'details': str(e)
        }), 500
    except Exception as e:
        print(f"General exception: {str(e)}")  # Debug log
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'An error occurred',
            'details': str(e)
        }), 500

@app.route('/')
def index():
    """Serve the main index.html file"""
    return send_file('index.html')

@app.route('/login')
def login():
    """Serve the login page"""
    return send_file('login.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files (CSS, JS, images, etc.)"""
    # Handle CSS files
    if path.startswith('css/'):
        return send_from_directory('.', path)
    # Handle JS files
    elif path.startswith('js/'):
        return send_from_directory('.', path)
    # Handle image files
    elif path.startswith('img/'):
        return send_from_directory('.', path)
    # Handle other static files
    else:
        try:
            return send_from_directory('.', path)
        except:
            return send_file('index.html')  # Fallback to index.html for SPA routing

if __name__ == '__main__':
    app.run(debug=True, port=5000)

