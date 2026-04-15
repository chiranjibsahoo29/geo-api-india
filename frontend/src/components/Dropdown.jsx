import React, { useEffect, useState } from "react";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL;
const API_KEY = import.meta.env.VITE_API_KEY;

function Dropdown() {
  const [states, setStates] = useState([]);
  const [districts, setDistricts] = useState([]);
  const [subdistricts, setSubdistricts] = useState([]);
  const [villages, setVillages] = useState([]);

  const [stateId, setStateId] = useState("");
  const [districtId, setDistrictId] = useState("");
  const [subdistrictId, setSubdistrictId] = useState("");
  const [villageId, setVillageId] = useState("");

  const [selectedStateName, setSelectedStateName] = useState("");
  const [selectedDistrictName, setSelectedDistrictName] = useState("");
  const [selectedSubdistrictName, setSelectedSubdistrictName] = useState("");
  const [selectedVillageName, setSelectedVillageName] = useState("");


  useEffect(() => {
    axios
      .get(`${API_URL}/states`, {
        headers: { "X-API-Key": API_KEY },
      })
      .then((res) => {
        const data = res.data.data || res.data;
        setStates(data);
      })
      .catch((err) => console.log(err));
  }, []);


  useEffect(() => {
    if (!stateId) return;

    axios
      .get(`${API_URL}/districts?state_id=${stateId}`, {
        headers: { "X-API-Key": API_KEY },
      })
      .then((res) => {
        const data = res.data.data || res.data;
        setDistricts(data);

        setSubdistricts([]);
        setVillages([]);

        setDistrictId("");
        setSubdistrictId("");
        setVillageId("");

        setSelectedDistrictName("");
        setSelectedSubdistrictName("");
        setSelectedVillageName("");
      })
      .catch((err) => console.log(err));
  }, [stateId]);


  useEffect(() => {
    if (!districtId) return;

    axios
      .get(`${API_URL}/subdistricts?district_id=${districtId}`, {
        headers: { "X-API-Key": API_KEY },
      })
      .then((res) => {
        const data = res.data.data || res.data;
        setSubdistricts(data);

        setVillages([]);

        setSubdistrictId("");
        setVillageId("");

        setSelectedSubdistrictName("");
        setSelectedVillageName("");
      })
      .catch((err) => console.log(err));
  }, [districtId]);


  useEffect(() => {
    if (!subdistrictId) return;

    axios
      .get(`${API_URL}/villages?subdistrict_id=${subdistrictId}`, {
        headers: { "X-API-Key": API_KEY },
      })
      .then((res) => {
        const data = res.data.data || res.data;
        setVillages(data);

        setVillageId("");
        setSelectedVillageName("");
      })
      .catch((err) => console.log(err));
  }, [subdistrictId]);

  return (
    <div className="dropdown-grid">
      <div className="full"></div>


      <div>
        <label>State</label>
        <select
          value={stateId}
          onChange={(e) => {
            const id = e.target.value;
            const name = e.target.options[e.target.selectedIndex].text;
            setStateId(id);
            setSelectedStateName(name);
          }}
        >
          <option value="">Select State</option>
          {[...states]
            .sort((a, b) => a.name.localeCompare(b.name))
            .map((s) => (
              <option key={s.id} value={s.id}>
                {s.name}
              </option>
            ))}
        </select>
      </div>


      <div>
        <label>District</label>
        <select
          value={districtId}
          onChange={(e) => {
            const id = e.target.value;
            const name = e.target.options[e.target.selectedIndex].text;
            setDistrictId(id);
            setSelectedDistrictName(name);
          }}
          disabled={!stateId}
        >
          <option value="">Select District</option>
          {[...districts]
            .sort((a, b) => a.name.localeCompare(b.name))
            .map((d) => (
              <option key={d.id} value={d.id}>
                {d.name}
              </option>
            ))}
        </select>
      </div>


      <div>
        <label>Subdistrict</label>
        <select
          value={subdistrictId}
          onChange={(e) => {
            const id = e.target.value;
            const name = e.target.options[e.target.selectedIndex].text;
            setSubdistrictId(id);
            setSelectedSubdistrictName(name);
          }}
          disabled={!districtId}
        >
          <option value="">Select Subdistrict</option>
          {[...subdistricts]
            .sort((a, b) => a.name.localeCompare(b.name))
            .map((sd) => (
              <option key={sd.id} value={sd.id}>
                {sd.name}
              </option>
            ))}
        </select>
      </div>


      <div>
        <label>Village</label>
        <select
          value={villageId}
          onChange={(e) => {
            const id = e.target.value;
            const name = e.target.options[e.target.selectedIndex].text;
            setVillageId(id);
            setSelectedVillageName(name);
          }}
          disabled={!subdistrictId}
        >
          <option value="">Select Village</option>
          {[...villages]
            .sort((a, b) => a.name.localeCompare(b.name))
            .map((v) => (
              <option key={v.id} value={v.id}>
                {v.name}
              </option>
            ))}
        </select>
      </div>


      {selectedVillageName && (
        <div className="selected full">
          <b>📍 Selected Address</b>
          <p>
            {selectedVillageName}, {selectedSubdistrictName},{" "}
            {selectedDistrictName}, {selectedStateName}, India
          </p>
        </div>
      )}
    </div>
  );
}

export default Dropdown;