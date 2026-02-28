import streamlit as st
import ccxt
import os
import time
from twilio.rest import Client
from dotenv import load_dotenv

# Page Config
st.set_page_config(page_title="Suga's Sentinel", page_icon="📈")
st.title("🛡️ Commodity Alpha Sentinel")

# --- ⚙️ STRATEGY CONFIG ---
SYMBOL = 'ETH/USDT'
ENTRY_PRICE = 2045.93 
STOP_LOSS = 1924.61
TAKE_PROFIT = 2288.57
RISK_USD = 50.0  # 1% of $5,000 account

# --- 🔑 CREDENTIALS (From Streamlit Secrets) ---
def get_secrets():
    return {
        "binance_key": st.secrets["BINANCE_API_KEY"],
        "binance_secret": st.secrets["BINANCE_SECRET_KEY"],
        "twilio_sid": st.secrets["TWILIO_ACCOUNT_SID"],
        "twilio_token": st.secrets["TWILIO_API_KEY"], # Use your Twilio Token/Secret
        "my_whatsapp": st.secrets["MY_WHATSAPP"]
    }

try:
    secrets = get_secrets()
    exchange = ccxt.binance({
        'apiKey': secrets["binance_key"],
        'secret': secrets["binance_secret"],
        'enableRateLimit': True,
    })

    # Sidebar Stats
    st.sidebar.header("📊 Account Strategy")
    st.sidebar.write(f"**Target Profit:** $400 (8%)")
    st.sidebar.write(f"**Risk per Trade:** ${RISK_USD} (1%)")

    # Live Data Fetching
    ticker = exchange.fetch_ticker(SYMBOL)
    current_price = ticker['last']
    gap = ENTRY_PRICE - current_price

    # Dashboard Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Price", f"${current_price}")
    col2.metric("Entry Target", f"${ENTRY_PRICE}")
    col3.metric("Gap to Entry", f"${gap:.2f}", delta_color="inverse")

    # Logic & Calculations
    st.subheader("🛡️ Sentinel Logic")
    if current_price >= ENTRY_PRICE:
        qty = RISK_USD / (ENTRY_PRICE - STOP_LOSS)
        st.success(f"🚀 **BREAKOUT DETECTED!**")
        st.write(f"**Recommended Quantity:** {qty:.4f} ETH")
        st.info("Manual Action Required on Binance App")
    else:
        st.warning(f"Waiting for Breakout... Market is ${gap:.2f} away from Entry.")

    # Risk Table
    st.table({
        "Parameter": ["Entry", "Stop Loss", "Take Profit", "Risk Amount"],
        "Value": [ENTRY_PRICE, STOP_LOSS, TAKE_PROFIT, f"${RISK_USD}"]
    })

except Exception as e:
    st.error(f"Setup Error: {e}")
    st.info("Please add your API Keys in Streamlit Cloud > Settings > Secrets")
