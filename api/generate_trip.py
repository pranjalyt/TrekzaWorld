from http.server import BaseHTTPRequestHandler
import json
import requests
import os

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        return
    
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Validate required fields
            required_fields = ['destination', 'boarding', 'duration', 'people', 'budgetMin', 'budgetMax']
            for field in required_fields:
                if field not in data or not data[field]:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': f'Missing required field: {field}'}).encode())
                    return
            
            # Get API key from environment
            OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '')
            
            if not OPENROUTER_API_KEY:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'error': 'OpenRouter API key not configured',
                    'message': 'Please set OPENROUTER_API_KEY environment variable in Vercel'
                }).encode())
                return
            
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
                'HTTP-Referer': self.headers.get('Referer', 'https://your-domain.vercel.app'),
                'X-Title': 'TrekzaWorld Travel Planner'
            }
            
            payload = {
                'model': 'openai/gpt-oss-20b:free',
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
            
            # Make request to OpenRouter
            response = requests.post('https://openrouter.ai/api/v1/chat/completions', 
                                   headers=headers, json=payload, timeout=30)
            
            if response.status_code != 200:
                self.send_response(response.status_code)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'error': 'Failed to generate itinerary',
                    'status_code': response.status_code,
                    'details': response.text
                }).encode())
                return
            
            result = response.json()
            
            # Extract the message content
            if 'choices' in result and len(result['choices']) > 0:
                message = result['choices'][0]['message']['content']
                
                if not message or len(message.strip()) == 0:
                    self.send_response(500)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        'error': 'Empty response from AI',
                        'raw_response': result
                    }).encode())
                    return
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'message': message}).encode())
            else:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'error': 'Unexpected response format from AI',
                    'details': result
                }).encode())
                
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'error': 'An error occurred',
                'details': str(e)
            }).encode())
