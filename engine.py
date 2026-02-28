import ccxt
import os
import time
import sys
from twilio.rest import Client
from dotenv import load_dotenv
from pathlib import Path

# --- 🛰️ SYSTEM FIXES ---
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# Smart path to find .env even if run from different folders
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# --- ⚙️ TRADING CONFIGURATION ---
SYMBOL = 'ETH/USDT'
ENTRY_PRICE = 2045.93 
STOP_LOSS = 1924.61
TAKE_PROFIT = ENTRY_PRICE + (ENTRY_PRICE - STOP_LOSS) * 2 
RISK_PER_TRADE = 50.0  # 1% of $5,000 account

# --- 🔑 CREDENTIALS ---
acc_sid = os.getenv('TWILIO_ACCOUNT_SID')
api_key = os.getenv('TWILIO_API_KEY')
api_secret = os.getenv('TWILIO_API_SECRET')
my_whatsapp = os.getenv('MY_WHATSAPP')

# --- 🏗️ INITIALIZE SERVICES ---
exchange = ccxt.binance({
    'apiKey': os.getenv('BINANCE_API_KEY'),
    'secret': os.getenv('BINANCE_SECRET_KEY'),
    'enableRateLimit': True
})

def send_whatsapp_alert(msg):
    try:
        client = Client(api_key, api_secret, acc_sid)
        client.messages.create(
            from_='whatsapp:+14155238886',
            body=msg,
            to=my_whatsapp
        )
        print("--- WhatsApp Alert Sent! ---")
    except Exception as e:
        print(f"WhatsApp Error: {e}")

def run_engine():
    print(f"--- Sentinel Engine Active: Monitoring {SYMBOL} ---")
    print(f"Target: {ENTRY_PRICE} | SL: {STOP_LOSS} | TP: {TAKE_PROFIT}")
    
    trade_executed = False
    
    while not trade_executed:
        try:
            ticker = exchange.fetch_ticker(SYMBOL)
            current_price = ticker['last']
            
            # 🚨 BREAKOUT TRIGGER
            if current_price >= ENTRY_PRICE:
                # Position Size Math
                qty = RISK_PER_TRADE / (ENTRY_PRICE - STOP_LOSS)
                
                alert_text = (
                    f"🚀 *SENTINEL: ETH BREAKOUT!*\n\n"
                    f"Price: ${current_price}\n"
                    f"Size: {qty:.4f} ETH\n"
                    f"Risk: $50 (Fixed)\n"
                    f"SL: ${STOP_LOSS} | TP: ${TAKE_PROFIT}"
                )
                
                print(f"BREAKOUT! Sending Alert...")
                send_whatsapp_alert(alert_text)
                
                # Note: Trade execution logic would go here
                trade_executed = True
                
            else:
                # \r updates the same line to keep terminal clean
                print(f"Market Stable: ${current_price} | Gap: ${ENTRY_PRICE - current_price:.2f}", end='\r')
            
            time.sleep(5)
            
        except Exception as e:
            print(f"\nEngine Error: {e}")
            break

if __name__ == "__main__":
    run_engine()