import os
from datetime import datetime
from typing import Any, Dict, Optional

from bson import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

load_dotenv()


class DatabaseUnavailableError(Exception):
    pass


class MongoService:
    def __init__(self) -> None:
        mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
        db_name = os.getenv("MONGO_DB_NAME", "ai_money_mentor")
        self.client = MongoClient(mongo_uri, serverSelectionTimeoutMS=3000)
        self.db = self.client[db_name]
        self.users = self.db["users"]
        self.financial_records = self.db["financial_records"]

    def save_record(self, feature: str, payload: Dict[str, Any], result: Dict[str, Any], user_id: str) -> None:
        """
        Best-effort write: app should still work even if DB is down.
        """
        try:
            record = {
                "user_id": ObjectId(user_id),
                "feature": feature,
                "input": payload,
                "output": result,
                "created_at": datetime.utcnow(),
            }
            self.financial_records.insert_one(record)
        except PyMongoError:
            # Ignore DB failures in MVP mode to avoid endpoint failure.
            return

    def find_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        try:
            return self.users.find_one({"email": email.lower().strip()})
        except PyMongoError as exc:
            raise DatabaseUnavailableError("Database unavailable") from exc

    def create_user(self, full_name: str, email: str, password_hash: str, role: str) -> Optional[Dict[str, Any]]:
        user_doc = {
            "full_name": full_name,
            "email": email.lower().strip(),
            "password_hash": password_hash,
            "role": role,
            "is_active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        try:
            insert_result = self.users.insert_one(user_doc)
            user_doc["_id"] = insert_result.inserted_id
            return user_doc
        except PyMongoError as exc:
            raise DatabaseUnavailableError("Database unavailable") from exc

    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        try:
            return self.users.find_one({"_id": ObjectId(user_id)})
        except PyMongoError:
            return None
        except Exception:
            return None

    def list_all_users(self) -> list[Dict[str, Any]]:
        try:
            return list(
                self.users.find(
                    {},
                    {
                        "password_hash": 0,
                    },
                ).sort("created_at", -1)
            )
        except PyMongoError as exc:
            raise DatabaseUnavailableError("Database unavailable") from exc

    def set_user_active(self, user_id: str, is_active: bool) -> bool:
        try:
            update = self.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"is_active": is_active, "updated_at": datetime.utcnow()}},
            )
            return update.matched_count > 0
        except PyMongoError as exc:
            raise DatabaseUnavailableError("Database unavailable") from exc
        except Exception:
            return False

