import pandas as pd

# Read the data
data = pd.read_csv("data.csv", header=None)

# Shuffle the data (random order each time)
data_shuffled = data.sample(frac=1).reset_index(drop=True)

# Save back to CSV
data_shuffled.to_csv("data.csv", header=False, index=False)

print(f"Data shuffled! Total rows: {len(data_shuffled)}")
print("\nLabel distribution:")
print(data_shuffled[0].value_counts().sort_index())
