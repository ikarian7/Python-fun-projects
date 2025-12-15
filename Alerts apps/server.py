from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/alert', methods=['POST'])
def alert():
    try:
        # Print the request to see what comes in
        print(f"Received request: {request.data}")

        # You can add more logic to handle the request here
        # For now, we'll just return a simple JSON response
        return jsonify({"message": "Alert received successfully!"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Error processing alert"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
