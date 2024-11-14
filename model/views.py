from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from tensorflow.keras.preprocessing import image
import numpy as np
import io
import tensorflow as tf
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from history.models import SearchHistory  # Import the SearchHistory model
from django.conf import settings
# Load the model
MODEL_PATH = settings.MODEL_PATH
model = tf.keras.models.load_model(MODEL_PATH)

# List of class names (ensure this matches the model output)
class_name = ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy', 
              'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy', 
              'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_', 
              'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot', 
              'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy', 
              'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy', 
              'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight', 
              'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy', 
              'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot', 
              'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 
              'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot', 
              'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus', 'Tomato___healthy']

def prepare_image(uploaded_file):
    img = image.load_img(io.BytesIO(uploaded_file.read()), target_size=(128, 128))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def make_prediction(img_array):
    predictions = model.predict(img_array)
    result_index = np.argmax(predictions, axis=1)[0]
    return int(result_index), predictions.tolist()

@csrf_exempt
@api_view(['POST'])  # Allow only POST requests to this endpoint
@permission_classes([IsAuthenticated])  # Ensure the user is authenticated
def predict_image(request):
    if 'image' in request.FILES:
        uploaded_file = request.FILES['image']
        img_array = prepare_image(uploaded_file)
        result_index, predictions = make_prediction(img_array)
        predicted_class_name = class_name[result_index]
        file_name = default_storage.save(uploaded_file.name, uploaded_file)
        file_path = default_storage.url(file_name)

        # Save to the history with the authenticated user
        SearchHistory.objects.create(
            user=request.user,  # Associate the history with the authenticated user
            predicted_class_name=predicted_class_name,
            predicted_class_index=result_index,
            predictions=predictions,
            image_url=file_path
        )

        return JsonResponse({
            'predicted_class_index': result_index,
            'predicted_class_name': predicted_class_name,
            'predictions': predictions,
            'image_url': file_path
        })
    else:
        return JsonResponse({'error': 'No image provided'}, status=400)
