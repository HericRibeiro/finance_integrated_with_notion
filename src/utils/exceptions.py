class MissingEnvironmentVariableError(Exception):
    """Variável obrigatória não encontrada no .env."""
    def __init__(self, var_name):
        super().__init__(f"Variável de ambiente obrigatória ausente: {var_name}")


class InvalidNotionTokenError(Exception):
    """Token da API inválido ou sem permissão."""
    pass


class NotionResourceNotFoundError(Exception):
    """Página ou recurso não encontrado no Notion."""
    def __init__(self, page_id):
        super().__init__(f"Página ou recurso não encontrado. PAGE_ID: {page_id}")


class NotionRateLimitError(Exception):
    """O Notion bloqueou temporariamente por excesso de requisições."""
    pass


class NotionServerError(Exception):
    """Erro interno no servidor do Notion (5xx)."""
    pass


class NotionParsingError(Exception):
    """Erro ao interpretar os dados retornados pela API."""
    def __init__(self, message):
        super().__init__(f"Erro ao processar dados do Notion: {message}")


class NotionClientError(Exception):
    """Erro genérico no cliente Notion."""
    pass
