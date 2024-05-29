from fastapi import FastAPI, UploadFile, HTTPException
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.imagenet_utils import decode_predictions
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from io import BytesIO
from google.cloud import firestore
import uvicorn
from google.cloud import storage as gcs
from firebase_admin import credentials, firestore, storage
import firebase_admin
import os

# Load labels
lines = []
labels = []
with open('model/classes_v2.txt') as f:
    lines = f.readlines()

for className in lines:
    labels.append(className.strip('\n'))

# Load the model
model = load_model('model/food_keras_v6.h5')

# Firestore client
db = firestore.Client()

app = FastAPI()

def upload_file_to_gcs(user_id: str, image_bytes: bytes, filename: str):
    bucket_name = "inifoodimage"
    storage_client = gcs.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(f'{user_id}/{filename}')

    blob.upload_from_string(image_bytes, content_type='image/jpeg')

    # Make the blob publicly viewable
    blob.make_public()

    return blob.public_url
#test
def predict(image_bytes: bytes, user_id: str, original_filename: str):
    try:
        image = Image.open(BytesIO(image_bytes))
        image = image.resize((128, 128))
        img_array = img_to_array(image)
        img_array = np.expand_dims(img_array, 0) 

        prediction = model.predict(img_array)
        predicted_class = labels[np.argmax(prediction)]
        confidence = np.max(prediction)

        food_ref = db.collection('foods').document(predicted_class)
        food = food_ref.get()

        if food.exists:
            food_data = food.to_dict()
            # Add result to foods-history subcollection
            user_ref = db.collection('users').document(user_id)
            food_history_doc_ref = user_ref.collection('foods-history').document()
            food_data['image_user'] = upload_file_to_gcs(user_id, image_bytes, original_filename)
            food_history_doc_ref.set(food_data)

            return {"nama": food_data['nama'], 
                    "kalori": food_data['kalori'], 
                    "satuan": food_data['satuan'],
                    "image_db": food_data['image_db'],
                    "image_user": food_data['image_user']}
        else:
            return {"error": f"{predicted_class} not found in database"}
    except Exception as e:
        return {"error": "The prediction is failed, please try again later or use different image"}

@app.post("/predict/{user_id}")
async def upload_image(user_id: str, file: UploadFile):
    try:
        image_bytes = await file.read()
        prediction = predict(image_bytes, user_id, file.filename)
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == '__main__': uvicorn.run(app, port=8080, host="0.0.0.0")