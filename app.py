#Happy Coding :(

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Gumloop API Configuration
GUMLOOP_API_URL = "https://api.gumloop.com/api/v1/start_pipeline"
GUMLOOP_API_KEY = "cc3520f10f6a4a4589714d7816253127"
USER_ID = "J60ZuQFOleXaC0CUDYAhXhVjgdV2"
SAVED_ITEM_ID = "cnGaNV6Mqr5u4veC88QGj5"

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
            "Authorization": f"Bearer {GUMLOOP_API_KEY}",
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


if __name__ == '__main__':
    app.run(debug=True)
