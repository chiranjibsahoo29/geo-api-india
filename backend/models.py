from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Text
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Country(Base):
    __tablename__ = "country"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class State(Base):
    __tablename__ = "state"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(String)
    country_id = Column(Integer, ForeignKey("country.id"))


class District(Base):
    __tablename__ = "district"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(String)
    state_id = Column(Integer, ForeignKey("state.id"))


class SubDistrict(Base):
    __tablename__ = "subdistrict"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(String)
    district_id = Column(Integer, ForeignKey("district.id"))


class Village(Base):
    __tablename__ = "village"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(String)
    subdistrict_id = Column(Integer, ForeignKey("subdistrict.id"))


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    business_name = Column(String, nullable=False)
    plan_type = Column(String, default="FREE")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    api_keys = relationship("ApiKey", back_populates="user")


class ApiKey(Base):
    __tablename__ = "apikey"

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, nullable=False)
    secret_hash = Column(String, nullable=False)
    key_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    daily_limit = Column(Integer, default=1000)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_used_at = Column(DateTime(timezone=True), nullable=True)

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="api_keys")

class ApiLog(Base):
    __tablename__ = "apilog"

    id = Column(Integer, primary_key=True)
    endpoint = Column(String)
    method = Column(String)
    status_code = Column(Integer)
    response_time = Column(Integer)  # ms
    api_key = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Lead(Base):
    __tablename__ = "lead"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    plan = Column(String, nullable=False, default="FREE")
    use_case = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())