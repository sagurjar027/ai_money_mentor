from fastapi import APIRouter, Depends, HTTPException, status

try:
    from backend.auth import create_access_token, get_current_admin, hash_password, verify_password
    from backend.db import DatabaseUnavailableError, MongoService
    from backend.models import LoginRequest, SignupRequest, ToggleUserStatusRequest
except ModuleNotFoundError:
    from auth import create_access_token, get_current_admin, hash_password, verify_password
    from db import DatabaseUnavailableError, MongoService
    from models import LoginRequest, SignupRequest, ToggleUserStatusRequest

router = APIRouter()
db = MongoService()


@router.post("/signup")
def signup(data: SignupRequest):
    try:
        existing = db.find_user_by_email(data.email)
    except DatabaseUnavailableError:
        raise HTTPException(status_code=503, detail="Database not reachable. Check MONGO_URI and MongoDB.")
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    requested_role = data.role.lower().strip()
    role = "admin" if requested_role == "admin" else "user"

    try:
        user = db.create_user(
            full_name=data.full_name.strip(),
            email=data.email,
            password_hash=hash_password(data.password),
            role=role,
        )
    except DatabaseUnavailableError:
        raise HTTPException(status_code=503, detail="Database not reachable. Check MONGO_URI and MongoDB.")
    if not user:
        raise HTTPException(status_code=503, detail="Could not create user.")
    access_token = create_access_token({"sub": str(user["_id"]), "role": user["role"]})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user["_id"]),
            "full_name": user["full_name"],
            "email": user["email"],
            "role": user["role"],
            "is_active": user["is_active"],
        },
    }


@router.post("/login")
def login(data: LoginRequest):
    try:
        user = db.find_user_by_email(data.email)
    except DatabaseUnavailableError:
        raise HTTPException(status_code=503, detail="Database not reachable. Check MONGO_URI and MongoDB.")
    if not user or not verify_password(data.password, user.get("password_hash", "")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    if not user.get("is_active", True):
        raise HTTPException(status_code=403, detail="Your account is disabled")

    access_token = create_access_token({"sub": str(user["_id"]), "role": user["role"]})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user["_id"]),
            "full_name": user["full_name"],
            "email": user["email"],
            "role": user["role"],
            "is_active": user["is_active"],
        },
    }


@router.get("/admin/users")
def admin_list_users(_: dict = Depends(get_current_admin)):
    try:
        users = db.list_all_users()
    except DatabaseUnavailableError:
        raise HTTPException(status_code=503, detail="Database not reachable. Check MONGO_URI and MongoDB.")
    normalized = []
    for user in users:
        normalized.append(
            {
                "id": str(user["_id"]),
                "full_name": user.get("full_name"),
                "email": user.get("email"),
                "role": user.get("role", "user"),
                "is_active": user.get("is_active", True),
                "created_at": user.get("created_at"),
            }
        )
    return {"users": normalized}


@router.patch("/admin/users/{user_id}/status")
def admin_toggle_user(user_id: str, data: ToggleUserStatusRequest, _: dict = Depends(get_current_admin)):
    try:
        ok = db.set_user_active(user_id=user_id, is_active=data.is_active)
    except DatabaseUnavailableError:
        raise HTTPException(status_code=503, detail="Database not reachable. Check MONGO_URI and MongoDB.")
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User status updated", "user_id": user_id, "is_active": data.is_active}
