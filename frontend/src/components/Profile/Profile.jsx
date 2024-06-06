import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import axios from "axios";

export function Profile() {
  const [userData, setUserData] = useState({});
  const [totalTracks, setTotalTracks] = useState({});
  const [savedTracks, setSavedTracks] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get("http://localhost:5000/callback");
        const { data } = response;
        setUserData(data.user_data);
        setTotalTracks(data.saved_tracks);
        setSavedTracks(data.saved_tracks.items);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  return (
    <>
      <div>
        <h2>Perfil de usuario</h2>
        <p>Nombre: {userData.display_name}</p>
        <p>Número de pistas guardadas: {totalTracks.total}</p>
        <h3>Top 5 pistas guardadas:</h3>
        <ul>
          {savedTracks.map((track, index) => (
            <li key={index}>
              {track.track.name} -{" "}
              {track.track.artists.map((artist) => artist.name).join(", ")}
            </li>
          ))}
        </ul>
      </div>
      <Link to="/EncuestaPage">
        <button>Push me</button>
      </Link>
    </>
  );
}
