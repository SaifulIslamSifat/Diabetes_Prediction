from flask import Flask, render_template, request, jsonify
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

# Load the model and scaler
with open('classification_model.pkl', 'rb') as file:
    model = pickle.load(file)

with open('scalling.pkl', 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        features = []
        # Fetch form data
        field_names = ['pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
        for field in field_names:
            value = float(request.form[field])
            features.append(value)

        # Convert features to a numpy array and reshape
        input_features = np.array(features).reshape(1, -1)

        # Scale the input features
        scaled_features = scaler.transform(input_features)

        # Make prediction
        prediction = model.predict(scaled_features)

        # Prepare the prediction response
        result = 'The person is diabetic' if prediction[0] == 1 else 'The person is not diabetic'

        # Render result in a new HTML page
        return render_template('result.html', prediction_text=result)
    except ValueError as e:
        # Handle the case where a non-numeric value was entered
        field_name = str(e).split(": ")[1]
        return jsonify({'error': f'Invalid value for field: {field_name}. Please enter a numeric value.'}), 400
    except Exception as e:
        # Handle other unexpected errors
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
