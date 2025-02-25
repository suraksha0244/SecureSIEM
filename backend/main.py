from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import metrics

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router
app.include_router(metrics.router)
