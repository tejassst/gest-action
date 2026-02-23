class GestureClassifier:
    def __init__(self, model_file):
        import pickle

        with open(model_file, "rb") as f:
            self.model = pickle.load(f)

    def predict(self, vector): 
        return self.model.predict([vector])[0]
    
    def predict_with_probability(self, vector):
        probs = self.model.predict_proba([vector])[0]
        predicted_label = probs.argmax()
        confidence = probs[predicted_label]
        return predicted_label, confidence
    