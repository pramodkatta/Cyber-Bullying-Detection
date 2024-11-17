import pickle
from preprocessing.image_text_extraction import extract_text_from_image
from preprocessing.audio_text_extraction import extract_text_from_audio

# Load the trained text model
with open('models/text_model.pkl', 'rb') as f:
    text_model = pickle.load(f)

# List of offensive words for rule-based fallback
offensive_words = {"bitch", "stupid", "idiot", "dumb", "fool", "hate", "kill"}

def predict_text(input_text):
    """
    Predict whether the input text is Cyber Bullying or No Cyber Bullying.
    Includes a rule-based fallback for detecting offensive words.
    """
    # Rule-based fallback for offensive words
    if any(word in input_text.lower() for word in offensive_words):
        return "Cyber Bullying"

    # Use the trained model to make predictions
    prediction = text_model.predict([input_text])[0]

    return "Cyber Bullying" if prediction == "cyberbullying" else "No Cyber Bullying"

def predict_image(image_path):
    """
    Extract text from an image and predict whether it's Cyber Bullying.
    """
    text = extract_text_from_image(image_path)
    return predict_text(text)

def predict_audio(audio_path):
    """
    Extract text from an audio file and predict whether it's Cyber Bullying.
    """
    text = extract_text_from_audio(audio_path)
    return predict_text(text)
