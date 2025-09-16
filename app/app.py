import os
#Uncomment this part in Windows
#os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
from PIL import Image 
# import cv2  #fails
from keras.models import load_model
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

# UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


model =load_model('app/model.h5')
# print('Model loaded. Check http://127.0.0.1:5000/')

labels = {0: 'Healthy', 1: 'Powdery', 2: 'Rust'}

def getResult(image_path):
    img = load_img(image_path, target_size=(225,225))
    x = img_to_array(img)
    x = x.astype('float32') / 255.
    x = np.expand_dims(x, axis=0)
    predictions = model.predict(x)[0]
    return predictions

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']

        basepath = os.path.dirname(__file__)
        folder_path = os.path.join(basepath, 'uploads')

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        file_path = os.path.join(
            folder_path, secure_filename(f.filename))
        f.save(file_path)

        predictions=getResult(file_path)
        predicted_label = labels[np.argmax(predictions)]
        return str(predicted_label) 
   
    return None


if __name__ == '__main__':
    # app.run(debug=True)
    
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)