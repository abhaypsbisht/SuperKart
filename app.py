import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Initialize Flask app
sales_price_api = Flask("SuperKart Sales Forecasting")

# Load the trained Boston housing model
model = joblib.load("SuperKart_v1_0.joblib")

# Define a route for the home page
@sales_price_api.get('/')
def home():
    return "Welcome to the SuperKart Sales Forecasting API!"

# Define an endpoint to predict price for a single store
@sales_price_api.post('/v1/storesales')
def predict_sales_price():
    # Get JSON data from the request
    sales_data = request.get_json()

    # Extract relevant house features from the input data
    sample = {
        'Product Weight': sales_data['Product_Weight'],
        'Product Allocated Area': sales_data['Product_Allocated_Area'],
        'Product MRP': sales_data['Product_MRP'],
        'Store Establishment Year': sales_data['Store_Establishment_Year'],
        'Store Size': sales_data['Store_Size'],
        'Store Location City Type': sales_data['Store_Location_City_Type'],
        'Store Type': sales_data['Store_Type'],
        'Product Id': sales_data['Product_Id'],
        'Product Type': sales_data['Product_Type'],
        'Store Id': sales_data['Store_Id'],
        'Product Sugar Content': sales_data['Product_Sugar_Content'],
        'Product Store Sales Total': sales_data['Product_Store_Sales_Total']
    }

    # Convert the extracted data into a DataFrame
    input_data = pd.DataFrame([sample])

    # Make a prediction using the trained model
    prediction = model.predict(input_data).tolist()[0]

    # Return the prediction as a JSON response
    return jsonify({'Predicted_PSST': prediction})

# Define an endpoint to predict price for a batch of stores
@sales_price_api.post('/v1/storesalesbatch')
def predict_store_batch():
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the file into a DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for the batch data
    predictions = model.predict(input_data).tolist()

    # Add predictions to the DataFrame
    input_data['Predicted_PSST'] = predictions

    # Convert results to dictionary
    result = input_data.to_dict(orient="records")

    return jsonify(result)

# Run the Flask app in debug mode
if __name__ == '__main__':
    sales_price_api.run(debug=True)
