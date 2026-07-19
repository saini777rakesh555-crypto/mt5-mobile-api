from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# 1. Base route to prevent 404 on the main link
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "Online",
        "message": "Your private MT5 Mobile Gateway is successfully running!"
    })

# 2. Main route to handle commands from your phone
@app.route('/mobile-trade', methods=['POST'])
def mobile_trade():
    # Defensive check to make sure JSON data was actually sent
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"status": "Error", "message": "Missing JSON request body"}), 400
        
    action = data.get("action")
    symbol = data.get("symbol")
    
    print(f"Received mobile command: {action} {symbol}")
    
    return jsonify({
        "status": "Success",
        "received_action": action,
        "received_symbol": symbol,
        "message": "Gateway successfully processed the packet."
    })

if __name__ == '__main__':
    # CRITICAL: Render automatically assigns a random port via environmental variables
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
