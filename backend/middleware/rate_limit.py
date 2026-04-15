from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from db import SessionLocal
from models import ApiKey, ApiLog


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        method = request.method

        public_paths = {
            "/",
            "/docs",
            "/openapi.json",
            "/redoc",
            "/api/v1/request-access",
        }


        if method == "OPTIONS" or path in public_paths:
            return await call_next(request)


        if not path.startswith("/api/v1"):
            return await call_next(request)

        api_key_value = request.headers.get("x-api-key")

        if not api_key_value:
            return JSONResponse(
                status_code=401,
                content={"detail": "X-API-Key missing"}
            )

        db: Session = SessionLocal()

        try:
            api_key = db.query(ApiKey).filter(
                ApiKey.key == api_key_value,
                ApiKey.is_active == True
            ).first()

            if not api_key:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Invalid API key"}
                )

            today = datetime.utcnow().date()

            count = db.query(func.count(ApiLog.id)).filter(
                ApiLog.api_key == api_key_value,
                func.date(ApiLog.created_at) == today
            ).scalar()

            limit = api_key.daily_limit or 1000

            if count >= limit:
                return JSONResponse(
                    status_code=429,
                    content={
                        "success": False,
                        "error": "RATE_LIMIT_EXCEEDED",
                        "message": f"Daily limit reached ({limit}). Upgrade your plan 🚀"
                    }
                )

            response = await call_next(request)

            try:
                log = ApiLog(
                    api_key=api_key_value,
                    endpoint=path,
                    method=method,
                    status_code=response.status_code
                )
                db.add(log)
                db.commit()
            except Exception:
                db.rollback()

            return response

        finally:
            db.close()