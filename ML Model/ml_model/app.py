from flask import Flask, request, jsonify
from sentiment_analysis import perform_sentiment_analysis
import json
import os

app = Flask(__name__)

# Route to perform sentiment analysis on quiz responses
@app.route('/analyze_quiz', methods=['POST'])
def analyze_quiz():
    try:
        # Get quiz data from the request body
        data = request.get_json()
        responses = data.get('responses', [])

        if not responses:
            return jsonify({"error": "No responses provided"}), 400

        # Convert responses into text format for analysis
        input_text = "\n".join([f"{response['question']} - {response['answer']}" for response in responses])
        
        # Create a temporary file to hold the input text
        input_file = 'data/input.txt'
        with open(input_file, 'w') as f:
            f.write(input_text)
        
        # Path for the output file
        output_file = 'output/result.txt'
        
        # Perform sentiment analysis using the ML model
        perform_sentiment_analysis(input_file, output_file)

        # Read the output and return it in the response
        with open(output_file, 'r') as f:
            result = f.read()

        # Remove temporary files
        os.remove(input_file)

        return jsonify({"result": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
