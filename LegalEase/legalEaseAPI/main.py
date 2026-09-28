import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from legalEaseAPI.routes import router
from config import BACKEND_HOST, BACKEND_PORT

app = FastAPI(
    title="LegalEase AI Legal Document Generator API",
    description="Backend microservice handling Gemini-powered document drafting",
    version="1.0.0"
)

# Enable CORS for Streamlit / external clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Router
app.include_router(router)

@app.get("/")
def home():
    return {
        "status": "online",
        "service": "LegalEase AI Legal Document Generator API",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run("legalEaseAPI.main:app", host=BACKEND_HOST, port=BACKEND_PORT, reload=True)