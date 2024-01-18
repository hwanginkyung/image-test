from flask import Flask, render_template, request, jsonify
from PIL import Image
import base64
import io
import requests
from transformers import BlipProcessor, BlipForConditionalGeneration
from typing import Union
from fastapi import FastAPI, UploadFile

app = FastAPI()


# app = Flask(__name__)
def process_image_with_cpu_model(image):
    processor = BlipProcessor.from_pretrained("./model")
    model = BlipForConditionalGeneration.from_pretrained("./model")
    # raw_image = Image.open(requests.get(img_url, stream=True).raw).convert('RGB')
    inputs = processor(image, return_tensors="pt")
    out = model.generate(**inputs)
    answer = processor.decode(out[0], skip_special_tokens=True)

    return answer


# @app.get('/')
# def index():
#     return render_template('index.html')


@app.post("/upload")
async def create_upload_file(file: UploadFile):
    try:
        print("test")
        # image_data = request.form['image'].split(',')[1]
        image_data = await file.read()
        print("Received image data:", image_data)
        image = Image.open(io.BytesIO(image_data))
        # image = Image.open(io.BytesIO(base64.b64decode(image_data)))
        result_caption = process_image_with_cpu_model(image)
        return result_caption
    except Exception as e:
        print("Error:", str(e))
        return str(e)


if __name__ == "__main__":
    app.run(debug=True)
