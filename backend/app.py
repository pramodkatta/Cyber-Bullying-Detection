from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from .inference import predict_text, predict_image, predict_audio
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Serve the static files (CSS, JS)
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")


# Serve the index.html file for the root route
@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join("frontend", "index.html"))

# Define the input model for text prediction
class TextInput(BaseModel):
    text: str


@app.post("/predict/text")
async def predict_text_endpoint(input: TextInput):
    text = input.text
    print(f"Received input: {text}")  # Log the input
    prediction = predict_text(text)
    print(f"Prediction result: {prediction}")  # Log the prediction
    return {"prediction": prediction}


@app.post("/predict/image")
async def predict_image_endpoint(file: UploadFile = File(...)):
    # Save the uploaded image temporarily
    with open("temp_image.png", "wb") as buffer:
        buffer.write(file.file.read())
    # Run prediction
    prediction = predict_image("temp_image.png")
    return {"prediction": prediction}

@app.post("/predict/audio")
async def predict_audio_endpoint(file: UploadFile = File(...)):
    # Save the uploaded audio file temporarily
    with open("temp_audio.wav", "wb") as buffer:
        buffer.write(file.file.read())
    # Run prediction
    prediction = predict_audio("temp_audio.wav")
    return {"prediction": prediction}


