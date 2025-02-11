from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
from langdetect import detect
from googletrans import Translator

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Define the default URL for the API endpoint
url = "http://localhost:11434/api/chat"
translator = Translator()

def llama3(prompt, model_name):
    data = {
        "model": model_name,  # Use the model_name passed to the function
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
    # Make the POST request to the LLaMA API
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
    # Get the user input and model from the request
    user_input = request.json.get("message")
    model_name = request.json.get("model", "llama3.2")  # Default to "llama3.2" if no model is provided
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    # Detect the language of the user input
    input_language = detect(user_input)

    # Call the llama3 function with user input and the selected model
    model_response = llama3(user_input, model_name)
graph TD
    A[Start] --> B[Initialize Flask App]
    B --> C[Enable CORS]
    C --> D[Define URL and Translator]
    D --> E[Define llama3 Function]
    E --> F[Define Home Route]
    F --> G[Define Chat Route]
    G --> H[Get User Input and Model]
    H --> I{Is User Input Provided?}
    I -- No --> J[Return Error Response]
    I -- Yes --> K[Detect Input Language]
    K --> L[Call llama3 Function]
    L --> M{Is Input Language English?}
    M -- No --> N[Translate Model Response]
    M -- Yes --> O[Return Model Response]
    O --> P[End]

    style A fill:#f9f,stroke:#333,stroke-width:4px
    style P fill:#f9f,stroke:#333,stroke-width:4px    graph TD
        A[Start] --> B[Initialize Flask App]
        B --> C[Enable CORS]
        C --> D[Define URL and Translator]
        D --> E[Define llama3 Function]
        E --> F[Define Home Route]
        F --> G[Define Chat Route]
        G --> H[Get User Input and Model]
        H --> I{Is User Input Provided?}
        I -- No --> J[Return Error Response]
        I -- Yes --> K[Detect Input Language]
        K --> L[Call llama3 Function]
        L --> M{Is Input Language English?}
        M -- No --> N[Translate Model Response]
        M -- Yes --> O[Return Model Response]
        O --> P[End]
    
        style A fill:#f9f,stroke:#333,stroke-width:4px
        style P fill:#f9f,stroke:#333,stroke-width:4px
    # Translate the response to the detected language if necessary
    if input_language != 'en':
        model_response = translator.translate(model_response, dest=input_language).text

    return jsonify({"response": model_response})  # Return the model response

if __name__ == "__main__":
    app.run(debug=True)







