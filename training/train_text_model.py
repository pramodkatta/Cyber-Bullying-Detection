
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from utils.load_data import load_data, split_data

# Load and preprocess data
data = load_data("data/labeled_data.csv")
X_train, X_test, y_train, y_test = split_data(data)

# Define the pipeline
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(ngram_range=(1, 2),
                              stop_words=None, 
                              max_features=10000)),  # Use n-grams for better context
    ('clf', LogisticRegression(solver='liblinear', 
                               class_weight='balanced',
                               max_iter=200))  # Handle class imbalance
])

# Train the model
pipeline.fit(X_train, y_train)

# Save the model
with open('models/text_model.pkl', 'wb') as f:
    pickle.dump(pipeline, f)

# Evaluate the model
y_pred = pipeline.predict(X_test)
print(classification_report(y_test, y_pred))
