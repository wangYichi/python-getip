import socket, json, math
from flask import Flask, request, render_template
from binance.um_futures import UMFutures
from binance.lib.utils import config_logging
from binance.error import ClientError
from binance.helpers import round_step_size
import os

API_Key = os.environ.get('api_key')
API_Secret = os.environ.get('api_secret')
binance_symbol_BTC = "BTCUSDT"
binance_symbol_ETH = "ETHUSDT"

um_futures_client = UMFutures(key=API_Key, secret=API_Secret)

app = Flask(__name__)

def set_buy_orders(symbol: str, quantity: float):
    #pricebuy = get_rounded_price(symbol, price)

    try:
        response = um_futures_client.new_order(
            symbol=symbol,
            side="BUY",
            type="MARKET",
            quantity=quantity,
        )
    except ClientError as error:
        print("set_buy_orders fails!!")

def set_sell_orders(symbol: str, quantity: float):
    #pricebuy = get_rounded_price(symbol, price)

    try:
        response = um_futures_client.new_order(
            symbol=symbol,
            side="SELL",
            type="MARKET",
            quantity=quantity,
        )
    except ClientError as error:
        print("set_sell_orders fails!!")

def cancel_all_orders(symbol: str):
    try:
        response = um_futures_client.cancel_open_orders(
            symbol=symbol,
        )
    except ClientError as error:
        print("cancel_all_orders fails!!")
        

@app.route('/')
def hello():
    return {
        "code": "success",
        "message": "Hello world!",
        }

@app.route('/webhook', methods=['POST'])
def webhook():
    data = json.loads(request.data) 
    webhook_quantity = float(data['strategy']['order_contracts'])
    webhook_quantity = math.floor(webhook_quantity*1000)/1000.0
    print(data)
    print(webhook_quantity)
    
    if(data['passphrase'] == "wangyizhi"):
        if(data['ticker'] == "BTCUSDT.P"):
            if(data['strategy']['order_action'] == "sell" and data['strategy']['order_id'] != "Long STP" and data['strategy']['order_id'] != "Short STP"):
                set_sell_orders(binance_symbol_BTC, webhook_quantity)
            elif(data['strategy']['order_action'] == "buy" and data['strategy']['order_id'] != "Long STP" and data['strategy']['order_id'] != "Short STP"):
                set_buy_orders(binance_symbol_BTC, webhook_quantity)
            elif(data['strategy']['order_id'] == "Long STP" or data['strategy']['order_id'] == "Short STP"):
                cancel_all_orders(binance_symbol_BTC)
        elif(data['ticker'] == "ETHUSDT.P"):
            if(data['strategy']['order_action'] == "sell"):
                set_sell_orders(binance_symbol_ETH, webhook_quantity)
            elif(data['strategy']['order_action'] == "buy"):
                set_buy_orders(binance_symbol_ETH, webhook_quantity)
        return {
        "code": "success",
        "message": "Success",
        }
    else:
        return {
        "code": "error",
        "message": "Invaid passphrase",
        }