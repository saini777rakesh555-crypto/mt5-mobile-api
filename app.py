from flask import Flask, request, jsonify
import MetaTrader5 as mt5
import os

app = Flask(__name__)

# CONFIGURATION: Put your MT5 Demo Details Here
MT5_LOGIN = 109846975        # <-- Replace with your MT5 account number
MT5_PASSWORD = "V!5nIiKw"     # <-- Replace with your MT5 password
MT5_SERVER = "MetaQuotes-Demo"    # <-- Replace with your exact broker server name

def execute_trade(action, symbol, volume=0.01):
    # Initialize connection to terminal
    if not mt5.initialize():
        return {"success": False, "error": f"Terminal init failed: {mt5.last_error()}"}
    
    # Log into your demo account
    if not mt5.login(MT5_LOGIN, password=MT5_PASSWORD, server=MT5_SERVER):
        error_code = mt5.last_error()
        mt5.shutdown()
        return {"success": False, "error": f"Login failed: {error_code}"}
    
    # Determine order type
    order_type = mt5.ORDER_TYPE_BUY if action.upper() == "BUY" else mt5.ORDER_TYPE_SELL
    price = mt5.symbol_info_tick(symbol).ask if order_type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(symbol).bid
    
    # Build trade request packet
    trade_request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": order_type,
        "price": price,
        "deviation": 20,
        "magic": 999999,
        "comment": "Sent from Mobile API",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    
    # Send order to MT5 network
    result = mt5.order_send(trade_request)
    mt5.shutdown() # Clean up resources
    
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        return {"success": False, "error": f"Trade rejected: {result.comment} (Code: {result.retcode})"}
        
    return {"success": True, "order_id": result.order}

@app.route('/')
def home():
    return jsonify({"status": "Online", "message": "Gateway Live"})

@app.route('/mobile-trade', methods=['POST'])
def mobile_trade():
    data = request.json
    action = data.get("action") 
    symbol = data.get("symbol")
    volume = data.get("volume", 0.01) # Default lot size if not specified
    
    if not action or not symbol:
        return jsonify({"success": False, "error": "Missing action or symbol"}), 400
        
    trade_result = execute_trade(action, symbol, volume)
    
    if trade_result["success"]:
        return jsonify({
            "status": "Success",
            "message": f"Successfully opened {action} position for {symbol}!",
            "order_id": trade_result["order_id"]
        }), 200
    else:
        return jsonify({
            "status": "Failed",
            "message": trade_result["error"]
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
    
    
