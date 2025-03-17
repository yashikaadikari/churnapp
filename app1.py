import numpy as np
import pickle
import streamlit as st

# Load the trained Gradient Boosting model
with open("best_gb_model.pkl", "rb") as pickle_in:
    best_gb_model = pickle.load(pickle_in)

def predict_status(features):
    """Function to predict Connection Status using the Gradient Boosting model"""
    features_list = list(features.values())  # Convert dictionary values to a list
    prediction = best_gb_model.predict([features_list])
    return prediction[0]

def main():
    # HTML for styling
    html_temp = """
    <div style="background-color:blue;padding:10px">
    <h2 style="color:white;text-align:center;">CONNECTION STATUS PREDICTOR</h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)

    # Input fields for selected features
    OUTSTANDING = st.number_input("OUTSTANDING", min_value=0.000, step=0.001)
    NETWORK_AGE_MONTHS = st.number_input("NETWORK AGE MONTHS", min_value=3.0, step=0.1)
    AVG_QUOTA = st.number_input("AVG QUOTA", min_value=0.00, step=0.01)
    AVG_USAGE = st.number_input("AVG USAGE", min_value=0.00, step=0.01)
    AVG_RSRP = st.number_input("AVG RSRP", min_value=-140.0, step=0.1)  # Adjusted step
    PACKAGE_RENTAL = st.number_input("PACKAGE RENTAL", min_value=0.0, step=0.1)

    # Binary categorical inputs
    PAYER_TYPE_OUTSTANDING_PAYMASTERS = st.selectbox("PAYER TYPE OUTSTANDING PAYMASTERS", options=["Yes", "No"])
    SEG_CODE_SMB = st.selectbox("SEG CODE SMB", options=["Yes", "No"])
    CREDIT_TYPE_SME = st.selectbox("CREDIT TYPE SME", options=["Yes", "No"])
    CREDIT_TYPE_SMB = st.selectbox("CREDIT TYPE SMB", options=["Yes", "No"])
    CREDIT_TYPE_LTEE = st.selectbox("CREDIT TYPE LTEE", options=["Yes", "No"])
    CPE_MODEL_ZLT_S10 = st.selectbox("CPE MODEL ZLT S10", options=["Yes", "No"])
    CPE_MODEL_B310S_925 = st.selectbox("CPE MODEL B310s-925", options=["Yes", "No"])
    PACKAGE_ID_LTE_AD_I = st.selectbox("PACKAGE ID LTE_AD_I", options=["Yes", "No"])
    CONGESTION_STATUS_NOT_IMPACTED = st.selectbox("CONGESTION STATUS NOT IMPACTED", options=["Yes", "No"])  # Fixed spelling

    # Mapping categorical inputs to binary values
    binary_map = {"Yes": 1, "No": 0}

    # Convert input values to a feature array
    features = {
        "OUTSTANDING": OUTSTANDING,
        "NETWORK_AGE_MONTHS": NETWORK_AGE_MONTHS,
        "AVG_QUOTA": AVG_QUOTA,
        "AVG_USAGE": AVG_USAGE,
        "AVG_RSRP": AVG_RSRP,
        "PACKAGE_RENTAL": PACKAGE_RENTAL,
        "PAYER_TYPE_OUTSTANDING_PAYMASTERS": binary_map[PAYER_TYPE_OUTSTANDING_PAYMASTERS],
        "SEG_CODE_SMB": binary_map[SEG_CODE_SMB],
        "CREDIT_TYPE_SME": binary_map[CREDIT_TYPE_SME],
        "CREDIT_TYPE_SMB": binary_map[CREDIT_TYPE_SMB],
        "CREDIT_TYPE_LTEE": binary_map[CREDIT_TYPE_LTEE],
        "CPE_MODEL_ZLT_S10": binary_map[CPE_MODEL_ZLT_S10],
        "CPE_MODEL_B310s-925": binary_map[CPE_MODEL_B310S_925],
        "PACKAGE_ID_LTE_AD_I": binary_map[PACKAGE_ID_LTE_AD_I],
        "CONGESTION_STATUS_NOT_IMPACTED": binary_map[CONGESTION_STATUS_NOT_IMPACTED],
    }

    # When the 'Predict' button is clicked
    if st.button("Predict"):
        result = predict_status(features)
        status = "PD" if result == 1 else "C"
        st.success(f"The predicted CONNECTION STATUS is: {status}")

if __name__ == '__main__':
    main()
