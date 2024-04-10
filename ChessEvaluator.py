import os
import json
import numpy as np
from tensorflow.python.client import device_lib
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Disable oneDNN custom operations for consistent floating-point calculations
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Step 2: Load and Prepare the Data
input_data = []
target_data = []

file_path = 'lichess_db_eval_modified.jsonl'
print(f"Attempting to load data from {file_path}")

try:
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line)
            if 'board_position' in data and 'evals' in data and data['evals'][0]['pvs']:
                # Assuming we're interested in the 'cp' value of the first 'pvs' of the first 'evals'
                input_data.append(data['board_position'])
                if 'cp' in data["evals"][0]["pvs"][0]:
                    target_data.append(data['evals'][0]['pvs'][0]['cp'])
                else:
                    target_data.append(data['evals'][0]['pvs'][0]['mate'])




except FileNotFoundError:
    print(f"File {file_path} not found. Please check the file path.")
    exit()

# Check if any lines were processed
if not input_data or not target_data:
    print("No data loaded. Check the file's content.")
    print(f"Processed {len(input_data)} input entries and {len(target_data)} target entries.")
    exit()

input_data = np.array(input_data, dtype='int32')
target_data = np.array(target_data, dtype='float32')

print(f"Loaded {len(input_data)} entries.")
X_train, X_test, y_train, y_test = train_test_split(input_data, target_data, test_size=0.2, random_state=42)

# Step 3: Define and Compile the Model
model = Sequential([
    Dense(64, activation='relu', input_shape=(64,)),
    Dense(64, activation='relu'),
    Dense(1)  # Output layer: Predicting a single value
])

model.compile(optimizer='adam', loss='mean_squared_error')

# Step 4: Train the Model
model.fit(X_train, y_train, epochs=10, validation_split=0.1)

# Step 5: Evaluate the Model
test_loss = model.evaluate(X_test, y_test)
print(f"Test loss: {test_loss}")

# Save the model
model.save('chess_model.keras')

# Output to indicate where the model is saved
print("Model saved in the chess_model directory.")
