from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set the model name
model_name = "llama3.2"

# Define the URL for the API endpoint
url = "http://localhost:11434/api/chat"

def llama3(prompt):
    data = {
        "model": model_name,  # Use model_name variable
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False,
    }

    headers = {
        "Content-Type": "application/json"
    }

    # Make the POST request to the Ollama API
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
        return response.json().get("message", {}).get("content", "No content returned.")
    except requests.exceptions.RequestException as e:
        return f"Error communicating with the model: {e}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    # Get the user input from the request
    user_input = request.json.get("message")

    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    # Call the llama3 function with user input
    model_response = llama3(user_input)

    return jsonify({"response": model_response})  # Return the model response

if __name__ == "__main__":
    app.run(debug=True)







