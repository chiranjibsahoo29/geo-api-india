# 🇮🇳 Geo-API India
### A Scalable Indian Location Data API Platform

**Geo-API India** is a full-stack SaaS platform designed to provide structured, searchable, and hierarchical location data for India through REST APIs. It enables developers to retrieve states, districts, subdistricts, and villages, making location selection and address integration easier for applications.

The platform combines a **FastAPI backend, React frontend, and PostgreSQL database hosted on NeonDB**, with API authentication, rate limiting, usage logging, and an administrative analytics dashboard.

## 🚀 Key Features

- **Hierarchical Location Data:** Access location information through State → District → Subdistrict → Village.
- **RESTful API:** Retrieve structured location data through FastAPI endpoints.
- **Search & Autocomplete:** Find villages and display matching location suggestions.
- **Cascading Dropdowns:** Select locations step by step using dependent dropdown menus.
- **API Key Authentication:** Protect API endpoints using the `X-API-Key` request header.
- **Rate Limiting:** Control API usage with support for free and premium access plans.
- **Pagination:** Retrieve large village datasets in manageable pages.
- **API Usage Logging:** Track endpoint usage, HTTP methods, status codes, response times, and timestamps.
- **Admin Analytics Dashboard:** Monitor request statistics, response times, and endpoint activity.
- **Request Access Form:** Capture access requests from potential API users.
- **Responsive UI:** React-based interface with a modern glassmorphism design.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | REST API development |
| React.js | Frontend development |
| Axios | Frontend-to-backend communication |
| PostgreSQL (NeonDB) | Cloud database |
| SQLAlchemy | Database ORM |
| Recharts | Analytics and data visualization |
| HTML & CSS | UI styling |
| Render | Backend deployment |
| Vercel | Frontend deployment |

## 🏗️ System Architecture

```text
             User / Client Application
                       |
                       v
                React Frontend
                       |
                       v
                  FastAPI
                       |
          +------------+------------+
          |            |            |
          v            v            v
      API Key      Rate Limiting   Validation
    Authentication                 & Logging
          |            |            |
          +------------+------------+
                       |
                       v
                SQLAlchemy ORM
                       |
                       v
              PostgreSQL / NeonDB
                       |
          +------------+------------+
          |                         |
          v                         v
   Location Datasets          API Usage Logs
 (States to Villages)         & Analytics


## 📍 Location Data Hierarchy

Geo-API India organizes location data in a hierarchical structure:

```text
India
 └── State
      └── District
           └── Subdistrict
                └── Village


The hierarchical structure makes it easier for applications to retrieve relevant locations and build address-selection interfaces.

## 🔌 API Endpoints

The backend provides versioned API endpoints under `/api/v1`.

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/v1/states` | Retrieve states |
| GET | `/api/v1/districts?state_id={id}` | Retrieve districts for a state |
| GET | `/api/v1/subdistricts?district_id={id}` | Retrieve subdistricts for a district |
| GET | `/api/v1/villages` | Village data retrieval |
| GET | Search endpoint | Search and autocomplete locations |

*Note: Confirm the exact village and search endpoint paths against the current backend source code before publishing this table as final API documentation.*

### Example API Request

Retrieve states using Python:

```python
import requests

BASE_URL = "http://localhost:8000"
API_KEY = "YOUR_API_KEY"

headers = {
    "X-API-Key": API_KEY
}

response = requests.get(
    f"{BASE_URL}/api/v1/states",
    headers=headers,
    timeout=10
)

response.raise_for_status()
data = response.json()

print(data)
```

### Example Response

```json
{
  "success": true,
  "count": 2,
  "data": [
    {
      "id": 1,
      "name": "Andhra Pradesh"
    },
    {
      "id": 2,
      "name": "Assam"
    }
  ]
}
```

*Illustrative response only; the exact fields and records depend on the API's response schema and database.*

## ⚙️ Local Setup

### Prerequisites

- Python 3.10+
- Node.js and npm
- A PostgreSQL database or NeonDB account
- Git

### 1. Clone the repository

```bash
git clone https://github.com/chiranjibsahoo29/Geo-API-India.git
cd Geo-API-India
```

Replace the repository URL with the actual GitHub URL if the repository uses a different name.

### 2. Set up the backend

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

On Windows, activate the virtual environment using:

```bash
venv\Scripts\activate
```

### 3. Configure environment variables

Create a `.env` file in the backend directory using the variable names expected by your application.

```env
DATABASE_URL=your_neon_postgresql_connection_string
```

Keep database credentials and API secrets private. Never commit `.env` to GitHub.

### 4. Start the FastAPI server

Use the actual Python module containing your FastAPI `app` object:

```bash
uvicorn main:app --reload
```

If the entry-point file has another name or is inside a package, update the command accordingly.

Open the interactive API documentation at:

```text
http://localhost:8000/docs
```

### 5. Start the frontend

Navigate to the React frontend directory:

```bash
npm install
npm run dev
```

Configure the frontend API base URL according to your local backend and the environment-variable conventions used by the project.

## 🔐 Security & Usage Monitoring

Geo-API India incorporates several API management mechanisms:

- API key verification for protected routes.
- Rate limiting to manage request frequency.
- Request logging for monitoring API activity.
- Database-backed API usage records.
- Free and premium access-plan support.

**Security note:** Production deployments should also use appropriate CORS restrictions, secret management, input validation, and careful handling of API keys in logs.

## 📊 Admin Dashboard

The administrative dashboard provides visibility into API activity, including:

- Total API requests.
- Average or recorded response times.
- Endpoint usage statistics.
- HTTP status-code information.
- Usage logs and request trends.

These metrics help monitor performance and identify potential API issues.

## ☁️ Deployment

The intended deployment architecture uses:

- **Backend:** Render
- **Frontend:** Vercel
- **Database:** NeonDB PostgreSQL

Set production environment variables in the respective hosting platforms, configure the frontend to use the deployed backend URL, and ensure that database connectivity and CORS settings are configured correctly.

## 💼 Potential Use Cases

Geo-API India can support applications that need structured Indian location data, including:

- E-commerce address forms.
- Delivery and logistics platforms.
- Location-based search applications.
- Village-level data analysis.
- Business registration and customer onboarding forms.
- Applications requiring state, district, subdistrict, and village selection.

## 🗺️ Future Enhancements

Potential improvements include:

- Automated API key generation.
- Dedicated developer dashboard and usage quotas.
- Razorpay or Stripe payment integration.
- Redis caching for frequently requested locations.
- Role-based access control.
- PIN code, city, and postal address APIs.
- Improved API documentation and client SDKs.
- Expanded geographic coverage and data-quality validation.

## 👨‍💻 Author

**Chiranjib Sahoo**

B.Tech Computer Science & Engineering student interested in Python backend development, API engineering, and scalable software systems.

- GitHub: [@chiranjibsahoo29](https://github.com/chiranjibsahoo29)
- Project: Geo-API India

---

*Geo-API India — Making structured Indian location data easier to access and integrate.*

