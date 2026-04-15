import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";


const API_URL = import.meta.env.VITE_API_URL;
const API_KEY = import.meta.env.VITE_API_KEY;

function StatCard({ title, value }) {
  return (
    <div className="glass card stat-card">
      <h3>{title}</h3>
      <p>{value}</p>
    </div>
  );
}

function AdminDashboard() {
  const [summary, setSummary] = useState({
    total_villages: 0,
    total_requests: 0,
    avg_response_time: 0,
  });

  const [topStates, setTopStates] = useState([]);
  const [requestTrend, setRequestTrend] = useState([]);
  const [endpointStats, setEndpointStats] = useState([]);

  useEffect(() => {
    const headers = {
      "X-API-Key": API_KEY,
    };

    axios.get(`${API_URL}/admin/summary`, { headers })
      .then((res) => setSummary(res.data.data))
      .catch(console.error);

    axios.get(`${API_URL}/admin/top-states`, { headers })
      .then((res) => setTopStates(res.data.data))
      .catch(console.error);

    axios.get(`${API_URL}/admin/request-trend`, { headers })
      .then((res) => setRequestTrend(res.data.data))
      .catch(console.error);

    axios.get(`${API_URL}/admin/endpoints`, { headers })
      .then((res) => setEndpointStats(res.data.data))
      .catch(console.error);
  }, []);

  return (
    <div className="dashboard-page">
      <h1 className="dashboard-title">📊 Admin Dashboard</h1>

      <div className="stats-grid">
        <StatCard title="Total Villages" value={summary.total_villages} />
        <StatCard title="Total Requests" value={summary.total_requests} />
        <StatCard title="Avg Response Time (ms)" value={summary.avg_response_time} />
      </div>

      <div className="charts-grid">
        <div className="glass card chart-card">
          <h2>Top States by Village Count</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={topStates}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="state" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="glass card chart-card">
          <h2>Request Trend</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={requestTrend}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="day" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="count" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="glass card chart-card full-width">
          <h2>Requests by Endpoint</h2>
          <ResponsiveContainer width="100%" height={320}>
            <BarChart data={endpointStats}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="endpoint" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

export default AdminDashboard;