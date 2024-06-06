import React, { useState } from 'react';
import axios from 'axios';

export function EncuestaForm() {
  const [encuestaData, setEncuestaData] = useState({
    gustaLeerLibros: '',
    generosLiterarios: [],
    generosCinematograficos: [],
    actividadesHobbies: [],
    inOrOut: ''
  });

  const handleInputChange = (event) => {
    const { name, value, type } = event.target;
    if (type === 'checkbox') {
      const isChecked = event.target.checked;
      setEncuestaData(prevState => ({
        ...prevState,
        [name]: isChecked ? [...(prevState[name] || []), value] : (prevState[name] || []).filter(item => item !== value)
      }));
    } else {
      setEncuestaData(prevState => ({
        ...prevState,
        [name]: value
      }));
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    console.log(encuestaData);
    try {
      const response = await axios.post('http://localhost:5000/encuesta', encuestaData);
      console.log(response.data);
    } catch (error) {
      console.error('Error al enviar la encuesta:', error);
    }
  };
  

  return (
    <div>
      <h2>Encuesta para el Spotify picho</h2>
      <form onSubmit={handleSubmit}>

        <label>
          ¿Te gusta leer libros?
          <input type="radio" name="gustaLeerLibros" value="Sí" onChange={handleInputChange} /> Sí
          <input type="radio" name="gustaLeerLibros" value="No" onChange={handleInputChange} /> No
        </label>

        <label>
          ¿Cuáles son tus géneros literarios favoritos? (Selecciona hasta 2)
          <input type="checkbox" name="generosLiterarios" value="Novela" onChange={handleInputChange} /> Novela
          <input type="checkbox" name="generosLiterarios" value="CienciaFicción" onChange={handleInputChange} /> Ciencia ficción
          <input type="checkbox" name="generosLiterarios" value="Fantasía" onChange={handleInputChange} /> Fantasía
          <input type="checkbox" name="generosLiterarios" value="Misterio/Thriller" onChange={handleInputChange} /> Misterio/Thriller
          <input type="checkbox" name="generosLiterarios" value="Romance" onChange={handleInputChange} /> Romance
          <input type="checkbox" name="generosLiterarios" value="NoFicción" onChange={handleInputChange} /> No ficción
          <input type="checkbox" name="generosLiterarios" value="Historia" onChange={handleInputChange} /> Historia
        </label>

        <label>
          ¿Cuáles son tus géneros de películas o series favoritos? (Selecciona hasta 2)
          <input type="checkbox" name="generosCinematograficos" value="Acción" onChange={handleInputChange} /> Acción
          <input type="checkbox" name="generosCinematograficos" value="Comedia" onChange={handleInputChange} /> Comedia
          <input type="checkbox" name="generosCinematograficos" value="Drama" onChange={handleInputChange} /> Drama
          <input type="checkbox" name="generosCinematograficos" value="CienciaFicción" onChange={handleInputChange} /> Ciencia ficción
          <input type="checkbox" name="generosCinematograficos" value="Fantasía" onChange={handleInputChange} /> Fantasía
          <input type="checkbox" name="generosCinematograficos" value="Terror" onChange={handleInputChange} /> Terror
          <input type="checkbox" name="generosCinematograficos" value="Romance" onChange={handleInputChange} /> Romance
        </label>

        <label>
          ¿Cuáles de las siguientes actividades disfrutas en tu tiempo libre? (Selecciona hasta 2)
          <input type="checkbox" name="actividadesHobbies" value="Deportes" onChange={handleInputChange} /> Deportes
          <input type="checkbox" name="actividadesHobbies" value="Cocina" onChange={handleInputChange} /> Cocina
          <input type="checkbox" name="actividadesHobbies" value="Viajes" onChange={handleInputChange} /> Viajes
          <input type="checkbox" name="actividadesHobbies" value="Fotografía" onChange={handleInputChange} /> Fotografía
          <input type="checkbox" name="actividadesHobbies" value="Pintura/Dibujo" onChange={handleInputChange} /> Pintura/Dibujo
          <input type="checkbox" name="actividadesHobbies" value="Jardineria" onChange={handleInputChange} /> Jardineria
          <input type="checkbox" name="actividadesHobbies" value="Videojuegos" onChange={handleInputChange} /> Videojuegos
        </label>

        <label>
          ¿Prefieres actividades al aire libre o en interiores?
          <input type="radio" name="inOrOut" value="Aire libre" onChange={handleInputChange} /> Aire libre
          <input type="radio" name="inOrOut" value="Interiores" onChange={handleInputChange} /> Interiores
          <input type="radio" name="inOrOut" value="Ambos" onChange={handleInputChange} /> Ambos
        </label>

        <button type="submit">¡Terminé!</button>
      </form>
    </div>
  );
};
