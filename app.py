import streamlit as st
from predict import predict_churn

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="Customer Churn AI",
    page_icon="🚀",
    layout="wide"
)

# ==============================
# CUSTOM CSS
# ==============================
st.markdown("""
<style>
html, body, [class*="css"]  {
    font-family: 'Segoe UI', sans-serif;
}

/* Background */
.main {
    background: linear-gradient(135deg, #1f4037, #99f2c8);
}

/* Center main container */
.block-container {
    max-width: 1100px;
    margin: auto;
    padding-top: 2rem;
}

/* Glass Card */
.card {
    background: rgba(255, 255, 255, 0.15);
    padding: 25px;
    border-radius: 15px;
    backdrop-filter: blur(12px);
    box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
    transition: all 0.3s ease;
    margin-bottom: 20px;
    position: relative;
}

/* Pulse animation on hover */
@keyframes pulseGlow {
    0% {
        box-shadow: 0px 12px 25px rgba(0,0,0,0.3), 0 0 10px rgba(255,255,255,0.3);
    }
    50% {
        box-shadow: 0px 12px 25px rgba(0,0,0,0.3), 0 0 18px rgba(255,255,255,0.5);
    }
    100% {
        box-shadow: 0px 12px 25px rgba(0,0,0,0.3), 0 0 10px rgba(255,255,255,0.3);
    }
}

.card:hover {
    transform: translateY(-8px);
    animation: pulseGlow 1.2s infinite;
}

/* Card Header/Subheader */
.card h1, .card h3 {
    margin-top: 0;
    color: #ffffff;
    font-weight: 700;
}

.card h1 {
    font-size: 2.5rem;
    text-align: center;
    background: linear-gradient(90deg, #ff512f, #dd2476);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
}

.card h3 {
    font-size: 1.5rem;
    margin-bottom: 15px;
}

/* Inputs spacing inside card */
.card .stSlider, .card .stNumberInput, .card .stSelectbox {
    margin-bottom: 15px;
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg, #ff512f, #dd2476);
    color: white;
    font-size: 18px;
    font-weight: bold;
    border-radius: 12px;
    padding: 0.6rem 1.5rem;
    border: none;
    transition: 0.3s ease;
    width: 100%;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0px 8px 20px rgba(0,0,0,0.3);
}

/* Result Box */
.result-box {
    padding: 20px;
    border-radius: 12px;
    font-size: 20px;
    font-weight: 600;
    text-align: center;
}

.low-risk {
    background-color: #165c32;
    color: #56d550;
}

.medium-risk {
    background-color: #775913;
    color: white;
}

.high-risk {
    background-color: #7c2d24;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# MAIN TITLE CARD
# ==============================
st.markdown("""
<div class="card">
    <h1>🚀 Customer Churn AI</h1>
    <p style="color: #f1f1f1; text-align:center; font-size: 18px;">
        Predict customer retention risk using Machine Learning
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==============================
# INPUT SECTION
# ==============================
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="card"><h3>📊 Customer Info</h3>', unsafe_allow_html=True)
    tenure = st.slider("Tenure (Months)", 0, 72, 12)
    monthly_charges = st.number_input("Monthly Charges", 0.0, 200.0, 70.0)
    total_charges = st.number_input("Total Charges", 0.0, 10000.0, 1000.0)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card"><h3>📄 Service Details</h3>', unsafe_allow_html=True)
    contract = st.selectbox(
        "Contract Type",
        ["Month-to-month", "One year", "Two year"]
    )
    internet_service = st.selectbox(
        "Internet Service",
        ["DSL", "Fiber optic", "No"]
    )
    payment_method = st.selectbox(
        "Payment Method",
        [
            "Electronic check",
            "Mailed check",
            "Bank transfer (automatic)",
            "Credit card (automatic)"
        ]
    )
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================
# PREDICT BUTTON
# ==============================
if st.button("🔮 Predict Churn"):

    input_dict = {
        "tenure": tenure,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges,
        "Contract": contract,
        "InternetService": internet_service,
        "PaymentMethod": payment_method
    }

    prediction, churn_probability = predict_churn(input_dict)

    # ==============================
    # PREDICTION RESULT CARD
    # ==============================
    if churn_probability < 0.3:
        risk_class = "low-risk"
        risk_text = "🟢 Low Risk of Churn"
    elif churn_probability < 0.6:
        risk_class = "medium-risk"
        risk_text = "🟡 Medium Risk of Churn"
    else:
        risk_class = "high-risk"
        risk_text = "🔴 High Risk of Churn"

    st.markdown(f"""
    <div class="card">
        <h3>📈 Prediction Result</h3>
        <div class="result-box {risk_class}">
            {risk_text}<br>
            Churn Probability: {churn_probability:.2%}
        </div>
        <p style="color: #f1f1f1; text-align:center; font-size:14px; margin-top:10px;">
            Model powered by Machine Learning trained on Telco Customer Dataset.
        </p>
    </div>
    """, unsafe_allow_html=True)