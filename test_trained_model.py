import joblib
import numpy as np

# Load the trained model
model = joblib.load('data_trainning/trained_model.joblib')


# Function to make a prediction and return the probability
def predict_flood_probability(water_level):
    # Prepare the input data as a 2D array
    input_data = np.array([[water_level]])

    # Make the prediction probability
    probabilities = model.predict_proba(input_data)

    # The probability of the positive class (flood) is the second column
    flood_probability = probabilities[0][1]

    return flood_probability


print("Enter water levels to predict flood probabilities. Press Ctrl+C to stop.")

while True:
    try:
        # Input water level from terminal
        water_level = float(input("Enter the water level (meters): "))

        # Ensure the water level is within the expected range
        if water_level < 0.1 or water_level > 1.2:
            print("Water level must be between 0.1 and 1.2 meters. Please try again.")
            continue

        # Predict flood probability
        flood_probability = predict_flood_probability(water_level)

        print(f'When Water Level = {water_level} meters, Probability of Flood: {flood_probability * 100:.2f}%')

    except ValueError as e:
        print(f"Invalid input: {e}")
    except KeyboardInterrupt:
        print("\nProgram stopped by user.")
        break
