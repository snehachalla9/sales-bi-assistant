from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="AI Business Intelligence Assistant",
    description="Ask natural-language questions about sales data.",
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "AI Business Intelligence Assistant is running"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}