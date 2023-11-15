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
        preg = float(request.form['pregnancies'])
        glucose = float(request.form['glucose'])
        bp = float(request.form['blood_pressure'])
        st = float(request.form['skin_thickness'])
        insulin = float(request.form['insulin'])
        bmi = float(request.form['bmi'])
        dpf = float(request.form['dpf'])
        age = float(request.form['age'])

        # Append the features to the list
        features.extend([preg, glucose, bp, st, insulin, bmi, dpf, age])

        # Convert features to a numpy array and reshape
        input_features = np.array(features).reshape(1, -1)

        # Scale the input features
        scaled_features = scaler.transform(input_features)

        # Make prediction
        prediction = model.predict(scaled_features)

        # Prepare the prediction response
        if prediction[0] == 0:
            result = 'The person is not diabetic'
        else:
            result = 'The person is diabetic'

        # Render result in a new HTML page
        return render_template('result.html', prediction_text=result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
