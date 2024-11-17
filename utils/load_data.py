import pandas as pd
from sklearn.model_selection import train_test_split
import re

def clean_text(text):
    """
    Preprocess the input text by:
    - Converting to lowercase
    - Removing special characters, numbers, and extra whitespace
    """
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = text.strip()  # Remove leading/trailing whitespace
    return text

def load_data(file_path):
    """
    Load the dataset and preprocess the text.
    Assign labels for 'cyberbullying' and 'not_cyberbullying'.
    """
    df = pd.read_csv(file_path)

    # Map 'class' to 'label': 0, 1 -> 'cyberbullying', 2 -> 'not_cyberbullying'
    df['label'] = df['class'].apply(lambda x: 'cyberbullying' if x in [0, 1] else 'not_cyberbullying')

    # Clean the 'tweet' text
    df['tweet'] = df['tweet'].apply(clean_text)

    return df[['tweet', 'label']]

def split_data(df):
    """
    Split the dataset into training and testing sets.
    """
    X_train, X_test, y_train, y_test = train_test_split(df['tweet'], df['label'], test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test
