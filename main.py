from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.user_routes import router as user_router
from api.routes.chat_routes import router as chat_router
from config import settings

app = FastAPI(
    title="TalkHub API",
    description="Backend for TalkHub messaging application",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rotas
app.include_router(user_router)
app.include_router(chat_router)


@app.get("/")
async def root():
    """Endpoint raiz da API."""
    return {
        "service": "TalkHub API",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
