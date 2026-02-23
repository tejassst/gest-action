import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier # Import KNN
import pickle # "Saves my trained model"


data = pd.read_csv("data.csv", header=None) # dataframe: Creates a table of the data

X = data.iloc[:,1:].values # features
y = data.iloc[:,0].values # labels

# test_size is 20% of the whole data set
# random_state ensures reproducabilty
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = KNeighborsClassifier(n_neighbors=5) # Model looks at 5 clostest training samples for voting
model.fit(X_train, y_train)
accuracy = model.score(X_test, y_test)


with open("gesture_knn.pkl", "wb") as f:
    pickle.dump(model, f)