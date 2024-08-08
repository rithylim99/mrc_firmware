import numpy as np
import pandas as pd

# Set parameters
num_data_points = 2000
min_level = 0
max_level = 0.8
threshold = 0.4

# Generate random water levels
water_levels = np.random.uniform(min_level, max_level, num_data_points)

# Determine flood occurrence
flood_occurrence = (water_levels > threshold).astype(int)

# Create DataFrame
df = pd.DataFrame({
    'Water Level (m)': water_levels,
    'Flood Occurrence': flood_occurrence
})

# Save to CSV file
df.to_csv('water_level_data.csv', index=False)
