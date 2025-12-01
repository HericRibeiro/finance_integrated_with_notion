import os
import requests
from dotenv import load_dotenv
from src.utils.exceptions import (
    InvalidNotionTokenError,
    NotionResourceNotFoundError,
    NotionRateLimitError,
    NotionServerError,
    NotionClientError,
    MissingEnvironmentVariableError
)

load_dotenv()

class NotionClient:
    def __init__(self, token: str):
        if not token:
            raise InvalidNotionTokenError("Token Notion está vazio.")

        self.token = token
        self.base_url = os.getenv("API_NOTION")

        if not self.base_url:
            raise MissingEnvironmentVariableError("API_NOTION")

        self.base_url = self.base_url.rstrip("/")

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }

    def _handle_response(self, response, resource_id=None):
        code = response.status_code

        if code == 401:
            raise InvalidNotionTokenError("Token inválido ou sem permissão.")

        if code == 404:
            raise NotionResourceNotFoundError(resource_id)

        if code == 429:
            raise NotionRateLimitError("Você atingiu o limite de requisições.")

        if code >= 500:
            raise NotionServerError("Erro interno no Notion.")

        if code != 200:
            raise NotionClientError(f"Erro inesperado. Código {code} | {response.text}")

        return response.json()

    def _get_paginated_children(self, block_id: str):
        url = f"{self.base_url}/blocks/{block_id}/children?page_size=100"
        results = []

        while url:
            response = requests.get(url, headers=self.headers)
            data = self._handle_response(response, resource_id=block_id)

            results.extend(data.get("results", []))

            next_cursor = data.get("next_cursor")
            if next_cursor:
                url = f"{self.base_url}/blocks/{block_id}/children?page_size=100&start_cursor={next_cursor}"
            else:
                url = None

        return results

    def get_page_blocks_recursive(self, block_id: str, depth: int = 0, max_depth: int = 10):
        if depth >= max_depth:
            return []

        blocks = self._get_paginated_children(block_id)
        final = []

        for block in blocks:
            new_block = block.copy()

            if block.get("has_children"):
                new_block["children"] = self.get_page_blocks_recursive(
                    block["id"], 
                    depth + 1, 
                    max_depth
                )

            final.append(new_block)

        return final

    def get_page_blocks(self, page_id: str):
        return self.get_page_blocks_recursive(page_id)