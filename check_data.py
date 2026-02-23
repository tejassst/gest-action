import pandas as pd

data = pd.read_csv("data.csv")
data.columns = ["label"] + [f"f{i}" for i in range(63)]
print("Shape: ", data.shape)
print("\nLabel counts:")
print(data["label"].value_counts())

