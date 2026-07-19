from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/mobile-trade', methods=['POST'])
def mobile_trade():
    data = request.json
    action = data.get("action") 
    symbol = data.get("symbol") 
    
    print(f"Received mobile command: {action} {symbol}")
    
    return jsonify({
        "status": "Success",
        "message": f"Mobile trade request for {symbol} received."
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
  
