import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.routes import router as tracker_router
from app.core.exceptions import AppError
from app.core.logging import init_logging, get_logger
from dotenv import load_dotenv
from app.core.middleware import RateLimiter

load_dotenv()  # Load environment variables from .env file
init_logging()
logger = get_logger(__name__) # Initialize the logger
rate_limiter = RateLimiter(max_requests=30, time_window=60) # Initialize the rate limiter

app = FastAPI(title="Macro Tracker API",
              description="API for tracking daily macro intake by processing user input.",
              version="0.1.0")

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    logger.error("AppError handled: %s", exc.detail)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

@app.lifespan.on_event("startup")
async def on_startup():
    logger.info("Macro Tracker API startup complete")

@app.lifespan.on_event("shutdown")
async def on_shutdown():
    logger.info("Macro Tracker API shutdown")

# Set up CORS middleware
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "*")
origins = [origin.strip() for origin in allowed_origins_env.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Allow specified origins from environment variable
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def check_referer(request: Request, call_next):
    referer = request.headers.get("referer")
    allowed_domains = origins  # Use the same allowed origins for referer check
    
    if referer:
        if not any(domain in referer for domain in allowed_domains):
            raise HTTPException(status_code=403, detail="Forbidden: Invalid referer")
    
    return await call_next(request)

# Include the tracker router
app.include_router(tracker_router)