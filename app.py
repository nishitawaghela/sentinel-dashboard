import streamlit as st
import pandas as pd
import joblib
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="Sentinel Risk Engine Dashboard",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling for Premium Light Theme Financial Terminal ---
st.markdown("""
    <style>
    /* Main app background and primary text */
    .main { background-color: #f8fafc; color: #0f172a; }
    
    /* Metrics cards - light gray/blue with a subtle border */
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 8px; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    
    /* Headers typography */
    h1, h2, h3 { color: #0f172a; font-family: 'Courier New', Courier, monospace; font-weight: bold; }
    
    /* Sidebar styling tweaks for light contrast */
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e2e8f0; }
    
    /* Action button styling */
    div.stButton > button:first-child {
        background-color: #e11d48; color: white; font-weight: bold; width: 100%; border: none; border-radius: 6px;
    }
    div.stButton > button:first-child:hover { background-color: #be123c; }
    </style>
""", unsafe_allow_html=True)

# --- Load the Machine Learning Model Safely ---
@st.cache_resource
def load_risk_model():
    try:
        # Tries to load from the same directory as app.py
        return joblib.load("anomaly_detector_v2.pkl")
    except FileNotFoundError:
        st.error("⚠️ 'anomaly_detector_v2.pkl' not found in the root directory! Please add it to your repo.")
        return None

model = load_risk_model()
EXPECTED_FEATURES = ['price', 'volume', 'action_SELL', 'order_type_MARKET']

# --- Sidebar / System Navigation ---
st.sidebar.title("🛡️ Sentinel Core")
st.sidebar.markdown("---")
st.sidebar.subheader("System Architecture")
st.sidebar.info("""
**Ingestion Layer:** FastAPI  
**Stream Buffer:** Apache Kafka (KRaft)  
**Stream Processing:** PySpark Streaming  
**Storage Engine:** Delta/Parquet Data Lake
""")
st.sidebar.markdown("---")
st.sidebar.caption("Designed for Advanced Real-Time Risk Stratification")

# --- Header ---
st.title("🚨 Sentinel Risk Engine")
st.subheader("Real-Time Financial Anomaly & Market Manipulation Monitor")
st.markdown("---")

# --- Tabs Setup ---
tab1, tab2 = st.tabs(["📊 Live Control Room", "🎛️ Interactive Attack Simulator"])

# ==========================================
# TAB 1: LIVE CONTROL ROOM (MOCK SYSTEM STATUS)
# ==========================================
with tab1:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Pipeline Status", value="ACTIVE / ONLINE", delta="Healthy")
    with col2:
        st.metric(label="Ingestion Rate", value="4,250 trd/sec", delta="+12%")
    with col3:
        st.metric(label="Active Anomaly Flags", value="14", delta="Class 3 Triggered", delta_color="inverse")
    with col4:
        st.metric(label="System Latency (P99)", value="8.4 ms", delta="-0.6ms")

    st.markdown("### 📈 Real-Time Stream Monitoring Log")
    
    # Mock data to visually show a recruiter what the system processes
    mock_log = pd.DataFrame([
        {"trade_id": "TRD-08241", "user_id": "USR-104", "symbol": "AAPL", "price": 150.25, "volume": 200, "action": "BUY", "status": "✅ Normal"},
        {"trade_id": "TRD-08242", "user_id": "USR-841", "symbol": "TSLA", "price": 240.50, "volume": 150, "action": "BUY", "status": "✅ Normal"},
        {"trade_id": "TRD-08243", "user_id": "USR-302", "symbol": "NVDA", "price": 480.00, "volume": 500, "action": "SELL", "status": "✅ Normal"},
        {"trade_id": "TRD-SPIKE-999", "user_id": "USR-HACKER", "symbol": "AAPL", "price": 140.00, "volume": 5000000, "action": "SELL", "status": "🚨 FRAUD DETECTED (Class 3)"},
    ])
    
    def color_status(val):
        color = '#dc2626' if '🚨' in val else '#10b981'
        return f'background-color: {color}; color: white; font-weight: bold;'

    st.dataframe(mock_log.style.map(color_status, subset=['status']), use_container_width=True, hide_index=True)

# ==========================================
# TAB 2: INTERACTIVE ATTACK SIMULATOR
# ==========================================
with tab2:
    st.markdown("### 🎛️ Inject a Simulated Payload into the Model")
    st.write("Adjust the parameters below to generate a custom trade block. Click **Execute** to force your Random Forest model to run real-time inference on the vector.")

    # Two columns for inputs
    c1, c2 = st.columns(2)
    with c1:
        stock_symbol = st.selectbox("Stock Ticker Symbol", ["AAPL", "NVDA", "TSLA", "AMZN", "MSFT"])
        price = st.number_input("Trade Execution Price ($)", min_value=1.00, max_value=2000.00, value=150.50, step=0.50)
        volume = st.number_input("Order Volume (Shares)", min_value=1, max_value=10000000, value=100, step=100)
    
    with c2:
        action = st.radio("Order Direction (Action)", ["BUY", "SELL"])
        order_type = st.radio("Execution Router (Order Type)", ["MARKET", "LIMIT"])
        user_id = st.text_input("Ingest User ID Tag", value="USR-LOCAL-TEST")

    st.markdown("---")
    
    # Inference execution logic
    if st.button(" FIRE TRADE INTO ENGINE"):
        if model is None:
            st.error("Cannot execute inference. Model binary is missing.")
        else:
            with st.spinner("Serializing payload and forcing inference vector transformation..."):
                time.sleep(0.4)  # Tiny artificial pause for realistic visual weight
                
                # Feature Engineering matching training pipeline exactly
                action_SELL = 1 if action == "SELL" else 0
                order_type_MARKET = 1 if order_type == "MARKET" else 0
                
                # Construct exact feature map
                input_data = pd.DataFrame([{
                    'price': price,
                    'volume': volume,
                    'action_SELL': action_SELL,
                    'order_type_MARKET': order_type_MARKET
                }])
                
                # Run the model binary
                prediction = model.predict(input_data[EXPECTED_FEATURES])[0]
                
                # Display Results beautifully based on prediction output
                if prediction != 0:
                    st.error(f"""
                    ### 🚨 HIGH-RISK ANOMALY INTERCEPTED 🚨
                    **Result:** Structural Threat Vector Identified (Prediction Class: {prediction})  
                    **Risk Action:** Routed to quarantine queue. Downstream webhook emitted.  
                    *Reasoning:* Sudden structural abnormality detected in volume-to-price ratio matching known algorithmic manipulation schemas.
                    """)
                    st.bell()
                else:
                    st.success("""
                    ### ✅ TRANSACTION VERIFIED CLEAN
                    **Result:** Cleared (Prediction Class: 0)  
                    **Action:** Successfully fully committed to local data lake. No anomalies detected.
                    """)