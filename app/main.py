from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as tracker_router

app = FastAPI(title="Macro Tracker API",
              description="API for tracking daily macro intake by processing user input.",
              version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the tracker router
app.include_router(tracker_router)