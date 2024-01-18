from flask import Flask, render_template, request, jsonify
from PIL import Image
import base64
import io
import requests
from transformers import BlipProcessor, BlipForConditionalGeneration

app = Flask(__name__)
def process_image_with_cpu_model(image):
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")
    #raw_image = Image.open(requests.get(img_url, stream=True).raw).convert('RGB')
    inputs = processor(image, return_tensors="pt")
    out = model.generate(**inputs)  
    return out

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        image_data = request.form['image'].split(',')[1]
        image = Image.open(io.BytesIO(base64.b64decode(image_data)))
        result_caption = process_image_with_cpu_model(image)
        return jsonify({"caption": result_caption})
    except Exception as e:
        return jsonify({"error": str(e)})
if __name__ == '__main__':
    app.run(debug=True)
