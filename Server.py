from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np

# Owen Michener
# Server.py
# April 19th, 2024
# This code is the server used to communicate between the java project and neural network

app = Flask(__name__)

# Load your pre-trained model
model = tf.keras.models.load_model('chess_model.keras')


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    print("Received data:", data)  # Debug print

    try:
        input_array = np.array(data['array'], dtype=np.int32)
        if input_array.shape[0] != 64:
            return jsonify({'error': 'Array must be of length 64'}), 400

        prediction = model.predict(input_array.reshape(1, 64))
        prediction = prediction.item()  # Ensuring it's a Python float

        print("Prediction:", prediction)  # Debug print
        return jsonify({'p': prediction})

    except Exception as e:
        return jsonify({'error': 'An error occurred: ' + str(e)}), 400  # More informative


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
