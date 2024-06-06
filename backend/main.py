from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from spotify_integration import SpotifyClient
import requests

app = Flask(__name__)
CORS(app)

# Instancia del cliente de Spotify
spotify_client = SpotifyClient(client_id="59cb9a527cfd43e2813e6d52b5f68aeb", client_secret="7387b7811f7348c28e2be0a72c730b38", redirect_uri="http://localhost:5000/callback")

songs_features = []

# Endpoints
@app.route("/", methods=["GET"])
def index():
    auth_url = spotify_client.get_authorize_url()
    return redirect(auth_url)

@app.route("/callback", methods=["GET"])
def callback():
    code = request.args.get('code')
    token_info = spotify_client.get_access_token(code)
    
    if token_info:
        access_token = token_info['access_token']
        sp = spotify_client.create_spotify_instance(access_token)

        # Datos del usuario (Profile)
        user_data = sp.current_user()
        saved_tracks = sp.current_user_saved_tracks(limit=5)

        process_saved_tracks(saved_tracks)
        
        return jsonify({
            'user_data': user_data,
            'saved_tracks': saved_tracks,
        })
    else:
        return jsonify({'error': 'No se pudo obtener el token de acceso'}), 400

def process_saved_tracks(saved_tracks):
    global songs_features
    songs_features = []
    for track in saved_tracks['items']:
        song_features = {
            'id': track['track']['id'],
            'name': track['track']['name'],
            'artists': [artist['name'] for artist in track['track']['artists']]
        }
        songs_features.append(song_features)





# Aqui empieza el error
def get_recommendations(survey_data, access_token, songs_features):
    base_url = 'https://api.spotify.com/v1/recommendations'

    last_saved_tracks = [song['id'] for song in songs_features[-5:]]

    params = {
        'limit': 5,
        'seed_tracks': ','.join(last_saved_tracks),
        'seed_genres': survey_data.get('seed_genres', ''),
        'target_energy': survey_data.get('target_energy', 0),
        'target_instrumentalness': survey_data.get('target_instrumentalness', 0),
        'target_popularity': survey_data.get('target_popularity', 50),
        'target_tempo': survey_data.get('target_tempo', 0),
    }
    
    headers = {
        'Authorization':f'Bearer {access_token}'
    }

    # Crear la cadena de consulta
    query_string = '&'.join([f"{key}={value}" for key, value in params.items()])

    full_url = f"{base_url}?{query_string}"

    response = requests.get(full_url, headers=headers)

    if response.status_code == 200:
        recommendations = response.json()
        return recommendations['tracks']
    else:
        print(f"Error al obtener recomendaciones: {response.status_code}")
        return None
# Y aquí termina




    # Otra manera de hacerlo pero tampoco sirve :)
    # if not songs_features:
    #     print("Error: No se encontraron características de canciones.")
    #     return None
    
    # last_saved_tracks = [song['id'] for song in songs_features[-5:]]

    # base_url = 'https://api.spotify.com/v1/recommendations'
    # params = {
    #     'market': 'US',
    #     'seed_tracks': ','.join(last_saved_tracks),
    #     'seed_genres': survey_data.get('seed_genres', ''),
    #     'target_energy': survey_data.get('target_energy', 0),
    #     'target_instrumentalness': survey_data.get('target_instrumentalness', 0),
    #     'target_popularity': survey_data.get('target_popularity', 50),
    #     'target_tempo': survey_data.get('target_tempo', 0),
    #     'limit': 5
    # }
    
    # # Filtrar los parámetros que tienen un valor diferente de 0 o cadena vacía
    # params = {key: value for key, value in params.items() if value != 0 and value != ''}

    # # Crear la cadena de consulta
    # query_string = '&'.join([f"{key}={value}" for key, value in params.items()])

    # full_url = f"{base_url}?{query_string}"

    # headers = {
    #     'Authorization': f'Bearer {access_token}'
    # }

    # response = requests.get(full_url, headers=headers)

    # if response.status_code == 200:
    #     recommendations = response.json()
    #     return recommendations['tracks']
    # else:
    #     print(f"Error al obtener recomendaciones: {response.status_code}")
    #     return None



    
    
# Endpoint para recibir y procesar los datos de la encuesta
@app.route('/recommendations', methods=['POST'])
def recommendations():
    try:
        survey_data = request.json
        print("Datos de la encuesta recibidos:", survey_data)
        
        if not survey_data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400

        access_token = spotify_client.get_access_token_from_cache()
        if access_token:
            recommendations = get_recommendations(survey_data, access_token, songs_features) 
            return jsonify({'recommendations': recommendations}), 200
        else:
            return jsonify({'error': 'No se pudo obtener el token de acceso'}), 400
        
    except Exception as e:
        print("Error al procesar la solicitud:", e)
        return jsonify({'error': 'Error al procesar la solicitud'}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
