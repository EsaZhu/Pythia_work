from flask import Flask, request, jsonify
import requests

from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# Gumloop API Configuration
GUMLOOP_API_URL = "https://api.gumloop.com/api/v1/start_pipeline"
GUMLOOP_API_KEY = "API_KEY_1234"
USER_ID = "USER_ID"
SAVED_ITEM_ID = "SAVED_ID"

@app.route('/classify_waste', methods=['POST'])
def classify_waste():
    """
    Classify the user's trash input using Gumloop API.
    """
    try:
        # Get the user's input from the request
        user_prompt = request.json.get('prompt', None)
        if not user_prompt:
            return jsonify({"error": "Prompt is required."}), 400

        # Prepare payload for Gumloop API
        payload = {
            "user_id": USER_ID,
            "saved_item_id": SAVED_ITEM_ID,
            "pipeline_inputs": [{"input_name": "waste_prompt", "value": user_prompt}]
        }
        headers = {
            "Authorization": f"Bearer cc3520f10f6a4a4589714d7816253127",
            "Content-Type": "application/json"
        }

        # Make a POST request to Gumloop API
        response = requests.post(GUMLOOP_API_URL, json=payload, headers=headers)

        # Check for successful response
        if response.status_code == 200:
            classification = response.json().get('classification', 'Unknown')
            # Respond to the user with the classification
            return jsonify({"response": f"This goes to the {classification}."})
        else:
            return jsonify({"error": "Failed to classify waste.", "details": response.text}), 500

    except Exception as e:
        return jsonify({"error": "An error occurred.", "details": str(e)}), 500


@app.route("/", methods=["GET"])
def home():
    """Simple route to verify that the server is running."""
    return jsonify({"message": "Waste Classification Chatbot is running!"})


if __name__ == "__main__":
    # Run the Flask server
    app.run(debug=True)
