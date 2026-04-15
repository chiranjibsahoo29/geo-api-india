import React, { useState } from "react";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL;
const API_KEY = import.meta.env.VITE_API_KEY;

function Search() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [selectedAddress, setSelectedAddress] = useState("");

  const handleSearch = async (e) => {
    const value = e.target.value;
    setQuery(value);

    if (value.trim().length < 2) {
      setResults([]);
      return;
    }

    try {
      const res = await axios.get(
        `${API_URL}/autocomplete?q=${encodeURIComponent(value)}`,
        {
          headers: {
            "X-API-Key": API_KEY,
          },
        }
      );

      setResults(res.data.data || []);
    } catch (err) {
      console.error("Autocomplete error:", err);
      setResults([]);
    }
  };

  const handleSelect = (item) => {
    setQuery(item.label);
    setSelectedAddress(item.fullAddress);
    setResults([]);
  };

  return (
    <div style={{ position: "relative" }}>
      <input
        type="text"
        placeholder="Search village..."
        value={query}
        onChange={handleSearch}
      />

      {results.length > 0 && (
        <div className="search-results">
          {results.map((item, index) => (
            <div
              key={index}
              className="search-item"
              onClick={() => handleSelect(item)}
            >
              <b>{item.label}</b>
              <div style={{ fontSize: "14px", color: "#cbd5e1", marginTop: "4px" }}>
                {item.fullAddress}
              </div>
            </div>
          ))}
        </div>
      )}

      {selectedAddress && (
        <div className="selected" style={{ marginTop: "16px" }}>
          <b>📍 Selected Address</b>
          <p>{selectedAddress}</p>
        </div>
      )}
    </div>
  );
}

export default Search;