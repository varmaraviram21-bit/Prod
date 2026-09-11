from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent

# serves any file under static/, including subfolders, at /static/...
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

users = []

class SignupRequest(BaseModel):
    name: str
    email: str
    password: str
    
class LoginRequest(BaseModel):
    email: str
    password: str
    
#frontend pages

@app.get("/")
def home():
    return FileResponse(BASE_DIR / "static" / "login.html")

@app.get("/signup")
def signup_page():
    return FileResponse(BASE_DIR / "static" / "signup.html")

@app.get("/index")
def python_practice():
    return FileResponse(BASE_DIR / "static" / "index.html")

#Signup API
@app.post("/api/signup")
def signup(user: SignupRequest):

    # Check whether email already exists
    for existing_user in users:
        if existing_user["email"] == user.email:
            return {
                "success": False,
                "message": "Email already registered"
            }

    # Store user temporarily
    users.append({
        "name": user.name,
        "email": user.email,
        "password": user.password
    })

    return {
        "success": True,
        "message": "Account created successfully"
    }
    
@app.post("/api/login")
def login(user: LoginRequest):

    for existing_user in users:

        if (
            existing_user["email"] == user.email
            and existing_user["password"] == user.password
        ):
            return {
                "success": True,
                "message": "Login successful",
                "name": existing_user["name"]
            }

    return {
        "success": False,
        "message": "Invalid email or password"
    }
