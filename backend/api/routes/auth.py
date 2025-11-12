from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, Body, Request
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy import text
from typing import Optional, Dict, Any
import requests

from ...database import engine
from ...config import settings

router = APIRouter()
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---------- DB ----------
USER_DDL = """
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  name TEXT,
  password_hash TEXT,
  picture TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
"""

def _ensure_user_table():
    with engine.begin() as con:
        con.execute(text(USER_DDL))

_ensure_user_table()

# ---------- JWT helpers ----------
def _create_access_token(data: dict, expires_minutes: int = settings.JWT_EXPIRES_MIN) -> str:
    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
def get_current_user(request: Request) -> Dict[str, Any]:
    auth = request.headers.get("authorization") or request.headers.get("Authorization")
    if not auth or not auth.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    token = auth.split(" ", 1)[1].strip()
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = payload.get("sub")
    email = payload.get("email")
    if not user_id or not email:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    return {"id": int(user_id), "email": email, "name": payload.get("name"), "picture": payload.get("picture")}
# ---------- Schemas ----------
class Signup(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None

class Login(BaseModel):
    email: EmailStr
    password: str
class SetPassword(BaseModel):
    new_password: str
    current_password: Optional[str] = None

class UpdateProfile(BaseModel):
    name: Optional[str] = None
    picture: Optional[str] = None
# ---------- Manual signup/login ----------
@router.post("/signup")
def signup(payload: Signup = Body(...)):
    _ensure_user_table()
    with engine.begin() as con:
        existing = con.execute(text("SELECT id FROM users WHERE email=:e"), {"e": payload.email}).mappings().first()
        if existing:
            raise HTTPException(status_code=409, detail="User already exists")
        ph = pwd_ctx.hash(payload.password)
        uid = con.execute(
            text("INSERT INTO users(email,name,password_hash) VALUES(:e,:n,:p) RETURNING id"),
            {"e": payload.email, "n": payload.name, "p": ph}
        ).scalar_one()
    token = _create_access_token({"sub": uid, "email": payload.email, "name": payload.name})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login")
def login(payload: Login = Body(...)):
    _ensure_user_table()
    with engine.begin() as con:
        row = con.execute(text("SELECT id,email,name,password_hash FROM users WHERE email=:e"), {"e": payload.email}).mappings().first()
        if not row or not row.get("password_hash") or not pwd_ctx.verify(payload.password, row["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = _create_access_token({"sub": row["id"], "email": row["email"], "name": row.get("name")})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
def me(user=Depends(get_current_user)):
    # include has_password
    with engine.begin() as con:
        row = con.execute(text("SELECT password_hash FROM users WHERE id=:id"), {"id": int(user["id"])}).mappings().first()
    has_password = bool(row and row.get("password_hash"))
    u = dict(user)
    u["has_password"] = has_password
    return {"user": u}

@router.post("/set_password")
def set_password(payload: SetPassword, user=Depends(get_current_user)):
    with engine.begin() as con:
        row = con.execute(text("SELECT password_hash FROM users WHERE id=:id"), {"id": int(user["id"])}).mappings().first()
        ph = row.get("password_hash") if row else None
        if ph:
            # existing password -> require current_password
            if not payload.current_password or not pwd_ctx.verify(payload.current_password, ph):
                raise HTTPException(status_code=400, detail="Current password is incorrect")
        new_hash = pwd_ctx.hash(payload.new_password)
        con.execute(text("UPDATE users SET password_hash=:ph WHERE id=:id"), {"ph": new_hash, "id": int(user["id"])})
    return {"ok": True}

@router.post("/update_profile")
def update_profile(payload: UpdateProfile, user=Depends(get_current_user)):
    with engine.begin() as con:
        con.execute(
            text("UPDATE users SET name=COALESCE(:n,name), picture=COALESCE(:p,picture) WHERE id=:id"),
            {"n": payload.name, "p": payload.picture, "id": int(user["id"])}
        )
    # return fresh user
    with engine.begin() as con:
        row = con.execute(text("SELECT email,name,picture FROM users WHERE id=:id"), {"id": int(user["id"])}).mappings().first()
    u = {"id": int(user["id"]), "email": row["email"], "name": row.get("name"), "picture": row.get("picture")}
    return {"user": u}
# ---------- Google OAuth ----------
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO = "https://www.googleapis.com/oauth2/v2/userinfo"
@router.get("/google/login")
def google_login():
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "online",
        "prompt": "consent",
    }
    from urllib.parse import urlencode
    return RedirectResponse(url=f"{GOOGLE_AUTH_URL}?{urlencode(params)}")

@router.get("/google/callback")
def google_callback(code: str):
    if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
        raise HTTPException(status_code=500, detail="Google OAuth not configured")
    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    tok = requests.post(GOOGLE_TOKEN_URL, data=data, timeout=20).json()
    if "access_token" not in tok:
        raise HTTPException(status_code=401, detail="Google token exchange failed")
    hdrs = {"Authorization": f"Bearer {tok['access_token']}"}
    prof = requests.get(GOOGLE_USERINFO, headers=hdrs, timeout=20).json()
    email = prof.get("email")
    if not email:
        raise HTTPException(status_code=401, detail="Google profile missing email")
    name = prof.get("name")
    picture = prof.get("picture")
    _ensure_user_table()
    with engine.begin() as con:
        row = con.execute(text("SELECT id,email,name FROM users WHERE email=:e"), {"e": email}).mappings().first()
        if row:
            uid = row["id"]
            con.execute(text("UPDATE users SET name=:n, picture=:p WHERE id=:id"),
                        {"n": name, "p": picture, "id": uid})
        else:
            uid = con.execute(text("INSERT INTO users(email,name,picture) VALUES(:e,:n,:p) RETURNING id"),
                              {"e": email, "n": name, "p": picture}).scalar_one()
    token = _create_access_token({"sub": uid, "email": email, "name": name, "picture": picture})
    # Post to opener if available; else redirect to frontend with token in hash
    fe = settings.FRONTEND_URL.rstrip("/")
    html = f"""
    <script>
      (function() {{
        const tok = {{"access_token": "{token}", "token_type":"bearer"}};
        try {{
          if (window.opener && !window.opener.closed) {{
            window.opener.postMessage(tok, "*");
            document.body.innerText = "Login successful. You can close this window.";
            return;
          }}
        }} catch (e) {{}}
        // same-tab fallback
        window.location.replace("{fe}/#access_token={token}");
      }})();
    </script>
    """
    return HTMLResponse(content=html)