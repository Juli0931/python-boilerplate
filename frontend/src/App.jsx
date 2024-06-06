import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { EncuestaForm, Profile } from "./components/index";
import "./App.css";

export default function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Profile />} />
          <Route path="/EncuestaPage" element={<EncuestaForm />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}
