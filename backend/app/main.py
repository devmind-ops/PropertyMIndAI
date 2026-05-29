import time
import uuid
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

app = FastAPI(
    title="PropertyMind API",
    description="Domain-aware document intelligence platform for real estate.",
    version="0.1.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware for Request ID and Timing
@app.middleware("http")
async def add_process_time_and_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    start_time = time.time()
    
    # Log incoming request
    logger.info(f"Request started: {request.method} {request.url.path} [ID: {request_id}]")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = str(process_time)
    
    logger.info(f"Request finished: {request.method} {request.url.path} [ID: {request_id}] - Time: {process_time:.4f}s")
    
    return response

@app.get("/health")
async def health_check():
    return {"status": "ok", "timestamp": time.time()}

@app.get("/")
async def root():
    return {
        "message": "Welcome to PropertyMind API",
        "docs": "/docs"
    }
