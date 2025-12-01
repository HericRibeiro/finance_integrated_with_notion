import os
from fastapi import HTTPException
from src.client.notion_client import NotionClient
from src.services.notion_service import NotionService
from src.utils.exceptions import (
    InvalidNotionTokenError,
    NotionResourceNotFoundError,
    MissingEnvironmentVariableError
)


class FinanceController:
    
    @staticmethod
    def get_finance_data():
        try:
            token = os.getenv("NOTION_TOKEN")
            page_id = os.getenv("NOTION_PAGE_ID")
            
            if not token:
                raise MissingEnvironmentVariableError("NOTION_TOKEN")
            
            if not page_id:
                raise MissingEnvironmentVariableError("NOTION_PAGE_ID")
            
            client = NotionClient(token)
            service = NotionService(client)
            
            data = service.get_finance_data(page_id)
            
            return data
            
        except InvalidNotionTokenError as e:
            raise HTTPException(status_code=401, detail=str(e))
        
        except NotionResourceNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        
        except MissingEnvironmentVariableError as e:
            raise HTTPException(status_code=500, detail=str(e))
        
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao buscar dados financeiros: {str(e)}"
            )
    
    @staticmethod
    def debug_blocks():
        try:
            token = os.getenv("NOTION_TOKEN")
            page_id = os.getenv("NOTION_PAGE_ID")
            
            if not token or not page_id:
                raise HTTPException(
                    status_code=500,
                    detail="Variáveis de ambiente não configuradas"
                )
            
            client = NotionClient(token)
            blocks = client.get_page_blocks_recursive(page_id)
            
            return {
                "total_blocks": len(blocks),
                "blocks": blocks
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))