import streamlit as st
import ccxt
import time

# Dashboard Title
st.title("🛡️ Suga's Sentinel (Public Mode)")

# Strategy Config
SYMBOL = 'ETH/USDT'
ENTRY_PRICE = 2045.93 
STOP_LOSS = 1924.61
RISK_USD = 50.0

# --- 🌐 PUBLIC INITIALIZATION ---
# Bina API Keys ke initialize kar rahe hain taaki Error 451 na aaye
exchange = ccxt.binance({'enableRateLimit': True})

try:
    # Sirf price fetch kar rahe hain (Ispe restriction kam hoti hai)
    ticker = exchange.fetch_ticker(SYMBOL)
    current_price = ticker['last']
    
    # Metrics display
    st.metric("Live ETH Price", f"${current_price}")
    st.write(f"**Target:** ${ENTRY_PRICE}")

    if current_price >= ENTRY_PRICE:
        # Simple Math for $5,000 account risk
        qty = RISK_USD / (ENTRY_PRICE - STOP_LOSS)
        st.success(f"🚀 BREAKOUT! Buy {qty:.4f} ETH manually on Binance App.")
    else:
        gap = ENTRY_PRICE - current_price
        st.info(f"Waiting... Gap to Entry: ${gap:.2f}")

except Exception as e:
    st.error(f"Abhi bhi block hai: {e}")
    st.warning("Lagta hai Streamlit ki poori range hi Binance ne block kar di hai.")

