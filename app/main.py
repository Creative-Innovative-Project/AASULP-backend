from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes import user
from app.routes import auth
from app.routes import semester
from app.routes import course
from app.routes import week
from app.routes import exam
from app.routes import topic
from app.routes import mainRoutes
from dotenv import load_dotenv
from jwt import ExpiredSignatureError, InvalidTokenError
import jwt
import os

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()


# To Prevent CORS Error
origins = [
    "http://localhost:5173",  # Vite dev server
    "http://127.0.0.1:5173",  # optional, just in case
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] for all origins (not safe for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Authentication Middleware
@app.middleware("http")
async def verify_token(request: Request, call_next):
    print("Middleware: Verifying token...")

    # Allow unauthenticated access for OPTIONS requests (CORS preflight)
    if request.method == "OPTIONS":
        return await call_next(request)

    if request.url.path in ["/docs", "/openapi.json", "/auth/login"]:
        return await call_next(request)

    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        request.state.user_id = payload.get("sub")
        if request.state.user_id is None:
            raise InvalidTokenError()
    except ExpiredSignatureError:
        return JSONResponse(status_code=401, content={"detail": "Token expired"})
    except InvalidTokenError:
        return JSONResponse(status_code=401, content={"detail": "Invalid token"})

    return await call_next(request)


# Base Route
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}


app.include_router(mainRoutes.router, prefix="/api/main", tags=["StartSemester"])
app.include_router(topic.router, prefix="/api", tags=["Topic"])
app.include_router(exam.router, prefix="/api", tags=["Exam"])
app.include_router(week.router, prefix="/api", tags=["Week"])
app.include_router(course.router, prefix="/api", tags=["Course"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(user.router, prefix="/api", tags=["Users"])
app.include_router(semester.router, prefix="/api", tags=["Semester"])
