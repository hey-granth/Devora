import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import settings
from .database import init_db
from .routers import auth, organizations, users

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting up Devora API...")
    await init_db()
    logger.info("Database initialized")

    yield

    # Shutdown
    logger.info("Shutting down Devora API...")


# Create FastAPI app
app = FastAPI(
    title="Devora API",
    description="AI-native Developer Relations Intelligence Platform",
    version="0.1.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Standardize HTTP exception responses."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "code": f"HTTP_{exc.status_code}",
            "details": getattr(exc, "details", {}),
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "code": "INTERNAL_ERROR",
            "details": {},
        },
    )


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "0.1.0"}


# Register routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(organizations.router, prefix="/api/v1/orgs", tags=["organizations"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.environment == "development",
    )
