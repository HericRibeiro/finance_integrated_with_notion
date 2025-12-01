# Finance API

API para gerenciamento de dados financeiros integrada com Notion.

## 🚀 Configuração

1. Clone o repositório
2. Crie um arquivo `.env` na raiz:
```env
NOTION_TOKEN=seu_token_aqui
NOTION_PAGE_ID=seu_page_id_aqui
API_NOTION=https://api.notion.com/v1
DEBUG=True
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute:
```bash
python main.py
```

## 📍 Endpoints

- `GET /api/finances` - Retorna dados financeiros do Notion
- `GET /api/debug/blocks` - Debug da estrutura de blocos

## 🔐 Variáveis de Ambiente

| Variável | Descrição |
|----------|-----------|
| `NOTION_TOKEN` | Token de integração do Notion |
| `NOTION_PAGE_ID` | ID da página de finanças |
| `API_NOTION` | URL da API do Notion |
| `DEBUG` | Modo debug (True/False) |