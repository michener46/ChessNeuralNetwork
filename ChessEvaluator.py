import csv
import os
import json
import numpy as np
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model

# Owen Michener
# ChessEvaluator.py
# April 19th, 2024
# This is the code used to train a neural network on chess using the
# data found on lichess.org.

# Disable oneDNN custom operations for consistent floating-point calculations
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Step 2: Load and Prepare the Data
input_data = []
target_data = []

file_path = 'lichess_db_eval_modified.jsonl'
filename = 'testing.csv'
i = 0
print(f"Attempting to load data from {file_path}")
with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        data = json.loads(line)
        if 'board_position' in data and 'evals' in data and data['evals'][0]['pvs']:
            if i == 0:
                print(data['board_position'])
            i += 1
            if i % 100000 == 0:
                print(i)
            # Assuming we're interested in the 'cp' value of the first 'pvs' of the first 'evals'
            input_data.append(data['board_position'])
            if 'cp' in data["evals"][0]["pvs"][0]:
                target_data.append(data['evals'][0]['pvs'][0]['cp'])
            else:
                target_data.append(data['evals'][0]['pvs'][0]['mate'])

input_data = np.array(input_data, dtype='int32')
target_data = np.array(target_data, dtype='float32')

print(f"Loaded {len(input_data)} entries.")
X_train, X_test, y_train, y_test = train_test_split(input_data, target_data, test_size=0.2, random_state=42)

# Step 3: Check if the model exists, load it; otherwise, define and compile a new one
model_path = 'chess_model.keras'
if os.path.exists(model_path):
    print("Loading existing model...")
    model = load_model(model_path)
else:
    print("Creating new model...")
    model = Sequential([
        Dense(64, activation='relu', input_shape=(64,)),
        Dense(64, activation='relu'),
        Dense(64, activation='relu'),
        Dense(64, activation='relu'),
        Dense(64, activation='relu'),
        Dense(64, activation='relu'),
        Dense(64, activation='relu'),
        Dense(64, activation='relu'),
        Dense(64, activation='relu'),
        Dense(64, activation='relu'),
        Dense(1)  # Output layer: Predicting a single value
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')

# Step 4: Train the Model
model.fit(X_train, y_train, batch_size = 4000, epochs=100, validation_split=0.1)

# Step 5: Evaluate the Model
test_loss = model.evaluate(X_test, y_test)
print(f"Test loss: {test_loss}")

# Save the model
model.save(model_path)

# Output to indicate where the model is saved
print(f"Model saved in {model_path}.")
