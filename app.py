import streamlit as st
import pandas as pd
import requests

# Streamlit UI for Boston Housing Price Prediction
st.title("SuperKart Sales Forecasting App")
st.write("This app accurately forecast the sales revenue of SuperKart outlets for the upcoming quarter.")
st.write("Move the sliders below to adjust values and get a prediction.")

# Collect user input using sliders
Product_Weight = st.slider("Weight of each product", 0.0, 25.0, 0.0, 0.01)
Product_Allocated_Area = st.slider("Ratio of the allocated display area of each product to the total display area of all the products in a store", 0.0, 1.0, 0.0, 0.001)
Product_MRP = st.slider("Maximum retail price of each product", 0.0, 300.0, 0.0, 1.0)
Store_Establishment_Year = st.slider("Nitric oxides concentration (NX)", 1980, 2020, 1980, 1)

# Categorical feature
# CHAS = st.selectbox("Charles River dummy variable (CHAS)", ["0 (No)", "1 (Yes)"])
# CHAS_value = 1 if CHAS.startswith("1") else 0

# Create input DataFrame
input_data = {
    'Product Weight': Product_Weight,
    'Product_Allocated_Area': Product_Allocated_Area,
    'Product MRP': Product_MRP,
    'Store Establishment Year': Store_Establishment_Year
}

if st.button("Forecast", type='primary'):
    response = requests.post("https://abhaypsbisht-Superkart.hf.space/v1/storesales", json=input_data)    # enter user name and space name before running the cell
    if response.status_code == 200:
        result = response.json()
        predicted_sales = result["Predicted_PSST"]
        st.success(f"🏡 Predicted Product Store Sales Total: **${predicted_sales}**")
    else:
        st.error("Error in API request")

# Batch Prediction
st.subheader("Batch Prediction")

file = st.file_uploader("Upload CSV file", type=["csv"])
if file is not None:
    if st.button("Predict for Batch", type='primary'):
        response = requests.post("https://abhaypsbisht-Superkart.hf.space/v1/storesalesbatch", files={"file": file})    # enter user name and space name before running the cell
        if response.status_code == 200:
            result = response.json()
            st.header("Batch Prediction Results")
            st.write(result)
        else:
            st.error("Error in API request")
