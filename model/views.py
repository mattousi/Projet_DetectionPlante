import io
import numpy as np
import tensorflow as tf
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from tensorflow.keras.preprocessing import image
from django.conf import settings
from django.core.files.storage import default_storage

# Charger le modèle à partir du chemin défini dans les paramètres
MODEL_PATH = settings.MODEL_PATH
model = tf.keras.models.load_model(MODEL_PATH)

# List of class names (replace with actual class labels used in your model)
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

# Fonction pour effectuer la prédiction d'image
def prepare_image(uploaded_file):
    """Prépare l'image téléchargée pour la prédiction."""
    # Convertir le fichier téléchargé en un flux de mémoire avec io.BytesIO
    img = image.load_img(io.BytesIO(uploaded_file.read()), target_size=(128, 128))  # Redimensionner l'image
    
    # Convertir l'image en un tableau numpy
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Ajouter la dimension du batch
    return img_array

def make_prediction(img_array):
    """Effectue la prédiction sur l'image donnée."""
    predictions = model.predict(img_array)
    result_index = np.argmax(predictions, axis=1)[0]  # Prendre l'index de la classe prédite
    return int(result_index), predictions.tolist()  # Convertir result_index en int natif

@csrf_exempt  # Désactive la protection CSRF si nécessaire
def predict_image(request):
    """Vue pour prédire la classe d'une image envoyée via POST."""
    if request.method == 'POST' and 'image' in request.FILES:
        # Récupérer l'image téléchargée
        uploaded_file = request.FILES['image']

        # Préparer l'image pour la prédiction
        img_array = prepare_image(uploaded_file)

        # Effectuer la prédiction
        result_index, predictions = make_prediction(img_array)

        # Récupérer le nom de la classe prédite
        predicted_class_name = class_name[result_index]

        # Enregistrer l'image dans le dossier défini par MEDIA_ROOT (si nécessaire)
        file_name = default_storage.save(uploaded_file.name, uploaded_file)
        file_path = default_storage.url(file_name)  # URL accessible de l'image

        # Retourner les résultats sous forme de réponse JSON
        return JsonResponse({
            'predicted_class_index': result_index,  # Index de la classe prédite
            'predicted_class_name': predicted_class_name,  # Nom de la classe prédite
            'predictions': predictions,  # Liste des prédictions
            'image_url': file_path  # URL de l'image téléchargée
        })
    else:
        return JsonResponse({'error': 'No image provided'}, status=400)
