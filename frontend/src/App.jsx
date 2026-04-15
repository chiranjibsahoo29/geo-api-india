import React from "react";
import Dropdown from "./components/Dropdown";
import Search from "./components/Search";
import AdminDashboard from "./components/AdminDashboard";
import Pricing from "./components/Pricing";
import RequestAccess from "./components/RequestAccess";
import "./App.css";

function App() {
  return (
    <div className="app">
      <div className="container">

        <h1 className="title">🌍 Geo API India</h1>


        <div className="glass card">
          <h2>🔍 Search Village</h2>
          <Search />
        </div>


        <div className="glass card">
          <h2>📍 Select Location</h2>
          <Dropdown />
        </div>


        <div className="glass card">
          <Pricing />
        </div>


        <div className="glass card">
          <RequestAccess />
        </div>


        <div className="glass card">
          <AdminDashboard />
        </div>

      </div>
    </div>
  );
}

export default App;