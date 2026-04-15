import React from "react";

function Pricing() {
  return (
    <div className="glass card">
      <h2>Pricing Plans</h2>

      <div style={{ display: "flex", gap: "20px", justifyContent: "center" }}>


        <div className="glass card" style={{ width: "250px" }}>
          <h3>Free</h3>
          <p>₹0 / month</p>
          <p>1000 requests/day</p>
          <button>Get Started</button>
        </div>


        <div className="glass card" style={{ width: "250px" }}>
          <h3>Starter</h3>
          <p>₹499 / month</p>
          <p>10,000 requests/day</p>
          <button>Upgrade</button>
        </div>


        <div className="glass card" style={{ width: "250px" }}>
          <h3>Pro</h3>
          <p>₹1999 / month</p>
          <p>100,000 requests/day</p>
          <button>Upgrade</button>
        </div>

      </div>
    </div>
  );
}

export default Pricing;