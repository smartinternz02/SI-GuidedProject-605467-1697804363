from PIL import Image
import io
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import tensorflow as tf
MODEL_PATH="model/alzheimer_cnn_model"
app = Flask(__name__)
CORS(app)

# Load your TensorFlow model
# model_path = 'model/alzheimer_detection.h5'
# model = tf.keras.models.load_model(model_path)

# def preprocess_image(image, target_size=(224, 224)):
#     # Load the image, resize it to the target size, and convert it to an array
#     img = tf.keras.preprocessing.image.load_img(image, target_size=target_size)
#     img_array = tf.keras.preprocessing.image.img_to_array(img)
#     # Expand the dimensions to match the model's expected input shape
#     img_array = np.expand_dims(img_array, axis=0)
#     # Preprocess the image (normalize values)
#     return tf.keras.applications.mobilenet.preprocess_input(img_array)

def image_to_buffer(image):
    buffer = io.BytesIO()
    image.save(buffer)  
    return buffer.getvalue()

def resize_img(img_buffer, size=(255, 255)):
    try:
        # Ensure the image format is compatible with PIL
        pil_image = Image.open(io.BytesIO(img_buffer)).resize(size).convert('RGB')
    except Exception as e:
        print(f"Error opening image: {e}")
        return None

    # Convert grayscale to RGB
    

    numpy_image = tf.keras.preprocessing.image.img_to_array(pil_image)
    tensor = tf.convert_to_tensor([numpy_image], dtype=tf.float32)

    return tensor


def image_to_tensor(image):
    image_buffer=image_to_buffer(image)
    tensor= resize_img(image_buffer,(176,176))
    return tensor

def predict(model_path,input_tensor):
    model = tf.keras.models.load_model(model_path, compile=False)
    predictions=model.predict(input_tensor)
    print(predictions)
    return predictions

@app.route("/",methods=['GET'])
def home():
    return jsonify({'msg':'You will do it'})
@app.route('/get-result', methods=['POST'])
def handle_api():
    image=request.files['image']
    
    tensor=image_to_tensor(image)
    print(tensor.shape)
    predictions=predict(MODEL_PATH,tensor)[0]
    predictions = [float(value) for value in predictions]
    print(predictions)
    predictions={
        "mild_demented":predictions[0],
        "moderate_demented":predictions[1],
        "non_demented":predictions[2],
        "very_mild_demented":predictions[3]
    }
    return jsonify({'class': predictions})


if __name__ == '__main__':
    app.run(debug=True, port=5000,host="localhost")
