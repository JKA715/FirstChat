from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Define the LM Studio server URL with the correct endpoint
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    
    # Payload for LM Studio's /v1/chat/completions endpoint
    payload = {
        "model": "openhermes-2.5-mistral-7b",  # Use the actual model ID
        "messages": [{"role": "user", "content": user_input}]
    }

    # Send the request to LM Studio
    response = requests.post(LM_STUDIO_URL, json=payload)
    
    # Extract the response text based on the LM Studio server's response format
    if response.status_code == 200:
        lm_response = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
    else:
        lm_response = "Error communicating with LM Studio"

    return jsonify({"response": lm_response})

if __name__ == '__main__':
    app.run(debug=True)
