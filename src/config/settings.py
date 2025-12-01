import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    NOTION_TOKEN: str = os.getenv("NOTION_TOKEN", "")
    NOTION_PAGE_ID: str = os.getenv("NOTION_PAGE_ID", "")
    API_NOTION: str = os.getenv("API_NOTION", "https://api.notion.com/v1")
    
    APP_NAME: str = "Finance API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    @classmethod
    def validate(cls):
        errors = []
        
        if not cls.NOTION_TOKEN:
            errors.append("NOTION_TOKEN não configurado")
        
        if not cls.NOTION_PAGE_ID:
            errors.append("NOTION_PAGE_ID não configurado")
        
        if errors:
            raise ValueError(f"Configuração inválida: {', '.join(errors)}")


settings = Settings()