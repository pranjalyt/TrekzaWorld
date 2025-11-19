# TrekzaWorld AI Travel Planner - Setup Guide

## Prerequisites
- Python 3.7 or higher
- OpenRouter API key (get one at https://openrouter.ai/)

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Set your OpenRouter API key:
```bash
# On macOS/Linux:
export OPENROUTER_API_KEY='your-api-key-here'

# On Windows:
set OPENROUTER_API_KEY=your-api-key-here
```

Or create a `.env` file in the project root (optional):
```
OPENROUTER_API_KEY=your-api-key-here
```

## Running the Application

1. Start the Flask backend:
```bash
python app.py
```

The Flask server will run on `http://localhost:5000`

2. Open `index.html` in your browser or serve it using a local server:
```bash
# Using Python's built-in server:
python -m http.server 8000
```

Then open `http://localhost:8000` in your browser.

## API Endpoint

- **POST** `/api/generate_trip`
- **Request Body:**
```json
{
  "destination": "Paris",
  "boarding": "Delhi",
  "duration": "5",
  "people": "2",
  "budgetMin": "50000",
  "budgetMax": "100000"
}
```

- **Response:**
```json
{
  "message": "Your AI-generated itinerary..."
}
```

## Notes

- Make sure CORS is enabled (already configured in app.py)
- The model can be changed in `app.py` (MODEL variable)
- If `gpt-oss-20b:free` is not available, the code uses `gpt-4o-mini` as fallback

