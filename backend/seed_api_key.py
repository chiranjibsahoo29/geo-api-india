from db import SessionLocal
from models import User, ApiKey
from auth_utils import generate_api_key, generate_api_secret, hash_secret


def main():
    db = SessionLocal()

    try:

        user = db.query(User).filter(User.email == "demo@geoapi.com").first()

        if not user:
            user = User(
                email="demo@geoapi.com",
                business_name="Demo Business",
                plan_type="FREE",
                is_active=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)


        api_key = generate_api_key()
        api_secret = generate_api_secret()

        new_key = ApiKey(
            key=api_key,
            secret_hash=hash_secret(api_secret),
            key_name="Development Key",
            user_id=user.id,
            is_active=True
        )

        db.add(new_key)
        db.commit()

        print("\nAPI KEY GENERATED")
        print(f"X-API-Key: {api_key}")
        print(f"X-API-Secret: {api_secret}")

    finally:
        db.close()


if __name__ == "__main__":
    main()