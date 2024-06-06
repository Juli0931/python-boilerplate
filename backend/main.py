# from flask import Flask, request, jsonify, redirect
# from flask_cors import CORS
# from spotify_integration import SpotifyClient

# app = Flask(__name__)
# CORS(app)

# # Instancia del cliente de Spotify
# spotify_client = SpotifyClient(client_id="59cb9a527cfd43e2813e6d52b5f68aeb", client_secret="aed7a9861d1040b1b7e1a9608ef503db", redirect_uri="http://localhost:5000/callback")

# # Endpoints de auth
# @app.route("/", methods=["GET"])
# def index():
#     auth_url = spotify_client.get_authorize_url()
#     return redirect(auth_url)

# @app.route("/callback", methods=["GET"])
# def callback():
#     code = request.args.get('code')
#     access_token = spotify_client.get_access_token(code)
#     sp = spotify_client.create_spotify_instance(access_token)

#     # Datos del usuario (Profile)
#     user_data = sp.current_user()
#     saved_tracks = sp.current_user_saved_tracks(limit=20)
    
#     return jsonify({
#         'user_data': user_data,
#         'saved_tracks': saved_tracks
#     })

# # Endpoint para recibir datos de encuesta
# @app.route('/encuesta', methods=['POST'])
# def recibir_encuesta():
#     try:
#         data = request.json
#         print("Datos de la encuesta recibidos:", data)
        
#         if not data:
#             return jsonify({'error': 'No se proporcionaron datos'}), 400

#         return jsonify({'message': 'Datos de la encuesta recibidos con éxito'}), 201
#     except Exception as e:
#         print("Error al procesar la solicitud:", e)
#         return jsonify({'error': 'Error al procesar la solicitud'}), 500

# if __name__ == "__main__":
#     app.run(debug=True, port=5000)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from spotify_integration import SpotifyClient

app = Flask(__name__)
CORS(app)

# Instancia del cliente de Spotify
spotify_client = SpotifyClient(client_id="59cb9a527cfd43e2813e6d52b5f68aeb", client_secret="aed7a9861d1040b1b7e1a9608ef503db", redirect_uri="http://localhost:5000/callback")

# Datos de encuesta
encuesta_data = []

# Endpoint de autenticación de Spotify
@app.route("/", methods=["GET"])
def index():
    auth_url = spotify_client.get_authorize_url()
    return redirect(auth_url)

# Endpoint de callback de Spotify
@app.route("/callback", methods=["GET"])
def callback():
    code = request.args.get('code')
    access_token = spotify_client.get_access_token(code)
    sp = spotify_client.create_spotify_instance(access_token)

    # Datos del usuario (Profile)
    user_data = sp.current_user()
    saved_tracks = sp.current_user_saved_tracks(limit=20)

    return jsonify({
        'user_data': user_data,
        'saved_tracks': saved_tracks
    })

# Endpoint para recibir datos de encuesta
@app.route('/encuesta', methods=['POST'])
def recibir_encuesta():
    try:
        data = request.json
        print("Datos de la encuesta recibidos:", data)
        
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400

        # Agregar los datos de la encuesta al registro global
        encuesta_data.append(data)

        return jsonify({'message': 'Datos de la encuesta recibidos con éxito'}), 201
    except Exception as e:
        print("Error al procesar la solicitud:", e)
        return jsonify({'error': 'Error al procesar la solicitud'}), 500

# Endpoint para obtener recomendaciones
@app.route('/recomendaciones', methods=['GET'])
def obtener_recomendaciones():
    try:
        # Obtener las preferencias del usuario desde la encuesta
        preferencias_usuario = encuesta_data[-1]  # Tomar la última encuesta recibida como ejemplo

        # Extraer las características relevantes de las canciones guardadas por el usuario
        saved_tracks = request.json['saved_tracks']
        canciones_guardadas = []
        for item in saved_tracks['items']:
            cancion = {
                'id': item['track']['id'],
                'nombre': item['track']['name'],
                'artista': item['track']['artists'][0]['name'],
                'genero': 'Pop'  # Supongamos que no tenemos información detallada sobre el género en este punto
            }
            canciones_guardadas.append(cancion)

        # Filtrar canciones basadas en géneros literarios y cinematográficos favoritos del usuario
        canciones_filtradas = [cancion for cancion in canciones_guardadas if cancion['genero'] in preferencias_usuario['generosLiterarios'] or
                               cancion['genero'] in preferencias_usuario['generosCinematograficos']]

        # Calcular la similitud entre las canciones filtradas y las preferencias del usuario
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform([cancion['genero'] + ' ' + cancion['artista'] for cancion in canciones_filtradas])
        user_preferences = tfidf_vectorizer.transform(preferencias_usuario['generosLiterarios'] + preferencias_usuario['generosCinematograficos'])
        cosine_similarities = cosine_similarity(user_preferences, tfidf_matrix).flatten()

        # Ordenar las canciones por similitud y obtener las recomendaciones
        recommendations_indices = cosine_similarities.argsort()[::-1]
        top_recommendations = [canciones_filtradas[idx] for idx in recommendations_indices[:5]]  # Obtener las 5 mejores recomendaciones

        return jsonify({'recomendaciones': top_recommendations}), 200
    except Exception as e:
        print("Error al procesar la solicitud:", e)
        return jsonify({'error': 'Error al procesar la solicitud'}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
