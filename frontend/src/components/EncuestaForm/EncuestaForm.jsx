import React, { useState } from 'react';
import axios from 'axios';

export function EncuestaForm() {
  const [encuestaData, setEncuestaData] = useState({
    genre: '',
    tempo: '',
    energy: '',
    instrumentalness: '',
    popularity: ''
  });

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setEncuestaData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    console.log(encuestaData);

    const mappedData = {
      seed_genres: encuestaData.genre,
      target_tempo: mapTempo(encuestaData.tempo),
      target_energy: mapEnergy(encuestaData.energy),
      target_instrumentalness: mapInstrumentalness(encuestaData.instrumentalness),
      target_popularity: mapPopularity(encuestaData.popularity)
    };

    try {
      const response = await axios.post('http://localhost:5000/recommendations', mappedData, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      console.log(response.data);
    } catch (error) {
      console.error('Error al enviar la encuesta:', error);
    }
  };

  const mapTempo = (tempo) => {
    switch (tempo) {
      case 'Lento': return 60; 
      case 'Medio': return 120; 
      case 'Rápido': return 180; 
      default: return 120;
    }
  };

  const mapEnergy = (energy) => {
    switch (energy) {
      case 'Alta energía': return 0.8;
      case 'Mediana energía': return 0.5;
      case 'Baja energía': return 0.2;
      default: return 0.5;
    }
  };

  const mapInstrumentalness = (instrumentalness) => {
    switch (instrumentalness) {
      case 'Principalmente con letra': return 0.1;
      case 'Equilibrio entre instrumentos y voz': return 0.5;
      case 'Mayormente instrumental': return 0.8;
      default: return 0.5;
    }
  };

  const mapPopularity = (popularity) => {
    switch (popularity) {
      case 'Populares': return 80;
      case 'Medianamente populares': return 50;
      case 'Menos populares': return 20;
      default: return 50;
    }
  };

  return (
    <div>
      <h2>Encuesta de Preferencias Musicales</h2>
      <form onSubmit={handleSubmit}>

        <label>
          ¿Qué tipo de música te gusta más?
          <select name="genre" value={encuestaData.genre} onChange={handleInputChange}>
            <option value="">Selecciona un género</option>
            <option value="pop">Pop</option>
            <option value="rock">Rock</option>
            <option value="hip-hop">Hip-Hop/Rap</option>
            <option value="electronic">Electrónica</option>
            <option value="jazz">Jazz</option>
            <option value="r&b">R&B/Soul</option>
            <option value="reggae">Reggae</option>
            <option value="folk">Folk</option>
            <option value="indie">Indie</option>
            <option value="metal">Metal</option>
          </select>
        </label>

        <label>
          ¿Qué ritmo prefieres?
          <select name="tempo" value={encuestaData.tempo} onChange={handleInputChange}>
            <option value="">Selecciona un ritmo</option>
            <option value="Lento">Lento</option>
            <option value="Medio">Medio</option>
            <option value="Rápido">Rápido</option>
          </select>
        </label>

        <label>
          ¿Qué nivel de energía te gusta en tu música?
          <select name="energy" value={encuestaData.energy} onChange={handleInputChange}>
            <option value="">Selecciona un nivel de energía</option>
            <option value="Alta energía">Alta energía</option>
            <option value="Mediana energía">Mediana energía</option>
            <option value="Baja energía">Baja energía</option>
          </select>
        </label>

        <label>
          ¿Prefieres música con letra o instrumental?
          <select name="instrumentalness" value={encuestaData.instrumentalness} onChange={handleInputChange}>
            <option value="">Selecciona una opción</option>
            <option value="Principalmente con letra">Principalmente con letra</option>
            <option value="Equilibrio entre instrumentos y voz">Equilibrio entre instrumentos y voz</option>
            <option value="Mayormente instrumental">Mayormente instrumental</option>
          </select>
        </label>

        <label>
          ¿Te gusta escuchar música popular o prefieres algo más desconocido?
          <select name="popularity" value={encuestaData.popularity} onChange={handleInputChange}>
            <option value="">Selecciona una opción</option>
            <option value="Populares">Populares</option>
            <option value="Medianamente populares">Medianamente populares</option>
            <option value="Menos populares">Menos populares</option>
          </select>
        </label>

        <button type="submit">¡Terminé!</button>
      </form>
    </div>
  );
}
