from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.controller.finance_controller import FinanceController
from src.config.settings import settings

# Valida configurações ao iniciar
settings.validate()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Finance API",
        "version": settings.APP_VERSION,
        "status": "online"
    }


@app.get("/api/finances")
def get_finances():
    """Retorna dados financeiros completos do Notion"""
    return FinanceController.get_finance_data()


@app.get("/api/debug/blocks")
def debug_blocks():
    """Debug: visualiza estrutura dos blocos"""
    return FinanceController.debug_blocks()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )