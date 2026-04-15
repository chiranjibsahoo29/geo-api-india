from fastapi import FastAPI, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, date
import time

from db import SessionLocal
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy import func,desc
from datetime import timedelta
from middleware.rate_limit import RateLimitMiddleware






from models import Village, SubDistrict, District, State, ApiKey, ApiLog, Lead

app = FastAPI()

app.add_middleware(RateLimitMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": "INTERNAL_SERVER_ERROR",
                    "message": str(e)
                }
            )



class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000"

        return response


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()

        response = await call_next(request)

        process_time = int((time.time() - start_time) * 1000)

        if request.method != "OPTIONS" and request.url.path.startswith("/api/v1"):
            db = SessionLocal()
            try:
                log = ApiLog(
                    endpoint=request.url.path,
                    method=request.method,
                    status_code=response.status_code,
                    response_time=process_time,
                    api_key=request.headers.get("x-api-key")
                )
                db.add(log)
                db.commit()
            except:
                pass
            finally:
                db.close()

        return response

app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(LoggingMiddleware)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_api_key(
    x_api_key: str = Header(None),
    db: Session = Depends(get_db)
):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="X-API-Key header missing")

    api_key = db.query(ApiKey).filter(
        ApiKey.key == x_api_key,
        ApiKey.is_active == True
    ).first()

    if not api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")

    api_key.last_used_at = datetime.utcnow()
    db.commit()

    return api_key



@app.get("/")
def home():
    return {"message": "GEO API RUNNING"}

@app.get("/api/v1/states")
def get_states(db: Session = Depends(get_db), api_key: ApiKey = Depends(verify_api_key)):
    data = db.query(State).order_by(State.name.asc()).all()
    return {"success": True, "count": len(data), "data": data}

@app.get("/api/v1/districts")
def get_districts(state_id: int, db: Session = Depends(get_db), api_key: ApiKey = Depends(verify_api_key)):
    data = db.query(District)\
        .filter(District.state_id == state_id)\
        .order_by(District.name.asc())\
        .all()
    return {"success": True, "count": len(data), "data": data}

@app.get("/api/v1/subdistricts")
def get_subdistricts(district_id: int, db: Session = Depends(get_db), api_key: ApiKey = Depends(verify_api_key)):
    data = db.query(SubDistrict)\
        .filter(SubDistrict.district_id == district_id)\
        .order_by(SubDistrict.name.asc())\
        .all()
    return {"success": True, "count": len(data), "data": data}

@app.get("/api/v1/villages")
def get_villages(subdistrict_id: int, page: int = 1, limit: int = 50,
                 db: Session = Depends(get_db), api_key: ApiKey = Depends(verify_api_key)):
    offset = (page - 1) * limit

    data = db.query(Village)\
        .filter(Village.subdistrict_id == subdistrict_id)\
        .order_by(Village.name.asc())\
        .offset(offset)\
        .limit(limit)\
        .all()

    return {"success": True, "count": len(data), "data": data}

@app.get("/api/v1/search")
def search(q: str, db: Session = Depends(get_db), api_key: ApiKey = Depends(verify_api_key)):
    if not q or q.strip() == "":
        return {"success": True, "count": 0, "data": []}

    results = db.query(
        Village.id,
        Village.name,
        SubDistrict.name.label("subdistrict"),
        District.name.label("district"),
        State.name.label("state")
    ).join(
        SubDistrict, Village.subdistrict_id == SubDistrict.id
    ).join(
        District, SubDistrict.district_id == District.id
    ).join(
        State, District.state_id == State.id
    ).filter(
        Village.name != None
    ).filter(
        Village.name.ilike(f"%{q.strip()}%")
    ).limit(20).all()

    data = [
        {
            "id": r.id,
            "name": r.name,
            "subdistrict": r.subdistrict,
            "district": r.district,
            "state": r.state
        }
        for r in results
    ]

    return {"success": True, "count": len(data), "data": data}
@app.get("/api/v1/autocomplete")
def autocomplete(q: str, limit: int = 10,
                 db: Session = Depends(get_db), api_key: ApiKey = Depends(verify_api_key)):
    if not q or q.strip() == "":
        return {"success": True, "count": 0, "data": []}

    q = q.strip()
    limit = min(limit, 10)

    results = db.query(
        Village.id,
        Village.name,
        SubDistrict.name.label("subdistrict"),
        District.name.label("district"),
        State.name.label("state")
    ).join(
        SubDistrict, Village.subdistrict_id == SubDistrict.id
    ).join(
        District, SubDistrict.district_id == District.id
    ).join(
        State, District.state_id == State.id
    ).filter(
        Village.name != None
    ).filter(
        Village.name.ilike(f"{q}%")
    ).order_by(
        Village.name.asc()
    ).limit(limit).all()

    data = [
        {
            "value": f"village_id_{r.id}",
            "label": r.name,
            "fullAddress": f"{r.name}, {r.subdistrict}, {r.district}, {r.state}, India"
        }
        for r in results
    ]

    return {"success": True, "count": len(data), "data": data}

@app.get("/api/v1/admin/summary")
def admin_summary(
    db: Session = Depends(get_db),
    api_key: ApiKey = Depends(verify_api_key)
):
    total_villages = db.query(func.count(Village.id)).scalar()
    total_requests = db.query(func.count(ApiLog.id)).scalar()
    avg_response_time = db.query(func.avg(ApiLog.response_time)).scalar() or 0

    return {
        "success": True,
        "data": {
            "total_villages": total_villages,
            "total_requests": total_requests,
            "avg_response_time": round(avg_response_time, 2)
        }
    }


@app.get("/api/v1/admin/top-states")
def admin_top_states(
    db: Session = Depends(get_db),
    api_key: ApiKey = Depends(verify_api_key)
):
    results = db.query(
        State.name,
        func.count(Village.id).label("village_count")
    ).join(
        District, District.state_id == State.id
    ).join(
        SubDistrict, SubDistrict.district_id == District.id
    ).join(
        Village, Village.subdistrict_id == SubDistrict.id
    ).group_by(
        State.name
    ).order_by(
        desc("village_count")
    ).limit(10).all()

    return {
        "success": True,
        "data": [
            {"state": r.name, "count": r.village_count}
            for r in results
        ]
    }


@app.get("/api/v1/admin/request-trend")
def admin_request_trend(
    db: Session = Depends(get_db),
    api_key: ApiKey = Depends(verify_api_key)
):
    results = db.query(
        func.date(ApiLog.created_at).label("day"),
        func.count(ApiLog.id).label("count")
    ).group_by(
        func.date(ApiLog.created_at)
    ).order_by(
        func.date(ApiLog.created_at)
    ).all()

    return {
        "success": True,
        "data": [
            {"day": str(r.day), "count": r.count}
            for r in results
        ]
    }


@app.get("/api/v1/admin/endpoints")
def admin_endpoints(
    db: Session = Depends(get_db),
    api_key: ApiKey = Depends(verify_api_key)
):
    results = db.query(
        ApiLog.endpoint,
        func.count(ApiLog.id).label("count")
    ).group_by(
        ApiLog.endpoint
    ).order_by(
        desc("count")
    ).all()

    return {
        "success": True,
        "data": [
            {"endpoint": r.endpoint, "count": r.count}
            for r in results
        ]
    }

@app.post("/api/v1/request-access")
def request_access(data: dict, db: Session = Depends(get_db)):
    name = data.get("name")
    email = data.get("email")
    plan = data.get("plan", "FREE")
    use_case = data.get("use_case", "")

    if not name or not email:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": "INVALID_INPUT",
                "message": "Name and email are required"
            }
        )

    existing = db.query(Lead).filter(Lead.email == email).first()

    if existing:
     return JSONResponse(
        status_code=409,
        content={
            "success": False,
            "error": "EMAIL_ALREADY_EXISTS",
            "message": "This email has already submitted a request"
        }
    )

    lead = Lead(
        name=name,
        email=email,
        plan=plan,
        use_case=use_case
    )

    db.add(lead)
    db.commit()
    db.refresh(lead)

    return {
        "success": True,
        "message": "Request received 🚀",
        "data": {
            "id": lead.id,
            "name": lead.name,
            "email": lead.email,
            "plan": lead.plan
        }
    }