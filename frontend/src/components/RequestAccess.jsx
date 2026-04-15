import React, { useState } from "react";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL;

function RequestAccess() {
  const [form, setForm] = useState({
    name: "",
    email: "",
    plan: "FREE",
    use_case: ""
  });

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await axios.post(`${API_URL}/request-access`, form);
      alert("Request sent successfully 🚀");
    } catch (err) {
      alert("Error sending request");
    }
  };

  return (
    <div className="glass card">
      <h2>🚀 Get API Access</h2>

      <form onSubmit={handleSubmit}>

        <input
          placeholder="Name"
          onChange={(e) => setForm({ ...form, name: e.target.value })}
        />

        <br /><br />

        <input
          placeholder="Email"
          onChange={(e) => setForm({ ...form, email: e.target.value })}
        />

        <br /><br />

        <select
          onChange={(e) => setForm({ ...form, plan: e.target.value })}
        >
          <option value="FREE">Free</option>
          <option value="STARTER">Starter</option>
          <option value="PRO">Pro</option>
        </select>

        <br /><br />

        <textarea
          placeholder="Use case..."
          onChange={(e) => setForm({ ...form, use_case: e.target.value })}
        />

        <br /><br />

        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

export default RequestAccess;