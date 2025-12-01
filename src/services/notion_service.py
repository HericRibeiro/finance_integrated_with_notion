from src.client.notion_client import NotionClient
from src.utils.notion_parser import NotionParser


class NotionService:
    
    def __init__(self, client: NotionClient):
        self.client = client
        self.parser = NotionParser()
    
    def get_finance_data(self, page_id: str) -> list:
        try:
            blocks = self.client.get_page_blocks_recursive(page_id)
            
            print(f"\n{'='*60}")
            print(f"📦 Total de blocos encontrados: {len(blocks)}")
            print(f"{'='*60}\n")
            
            months_data = self._process_months(blocks)
            summary_data = self._process_summary(blocks)
            
            print(f"\n{'='*60}")
            print(f"✅ Processamento concluído:")
            print(f"   📅 Meses processados: {len(months_data)}")
            print(f"   📊 Itens do resumo: {len(summary_data.get('items', []))}")
            print(f"{'='*60}\n")
            
            return [
                ["months", months_data],
                ["summary", summary_data]
            ]
        except Exception as e:
            print(f"\n❌ ERRO no get_finance_data: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def _process_months(self, blocks: list) -> list:
        months = []
        current_month_name = ""
        
        for i, block in enumerate(blocks):
            block_type = block.get("type")
            text = self.parser.extract_text(block)
            
            if block_type == "heading_2":
                clean_text = text.replace("🚀", "").strip()
                months_pt = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                           "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
                
                for month in months_pt:
                    if month in clean_text:
                        current_month_name = month
                        print(f"📌 Heading detectado: {month}")
                        break
            
            elif block_type == "to_do":
                if "/" in text and len(text.strip()) <= 10:
                    is_checked = block.get("to_do", {}).get("checked", False)
                    print(f"\n🔍 Bloco {i}: TO-DO com código '{text}' (checked={is_checked})")
                    
                    month_data = self._process_month_block(
                        block, 
                        text.strip(), 
                        current_month_name
                    )
                    
                    if month_data and month_data.get("items"):
                        months.append(month_data)
                        print(f"   ✅ Mês '{month_data.get('month')}' adicionado com {len(month_data.get('items', []))} itens")
                    else:
                        print(f"   ⚠️ Mês '{month_data.get('month') if month_data else 'desconhecido'}' sem itens")
        
        return months
    
    def _process_month_block(self, block: dict, code: str, month_name: str) -> dict:
        
        if not month_name:
            month_name = self._month_code_to_name(code)
        
        print(f"   📆 Processando: {month_name} ({code})")
        
        month_data = {
            "month": month_name,
            "code": code,
            "items": []
        }
        
        children = block.get("children", [])
        print(f"   Total de filhos: {len(children)}")
        
        for j, child in enumerate(children):
            child_type = child.get("type")
            
            if child_type in ["divider", "paragraph"]:
                continue
            
            item = self._process_item(child)
            if item:
                month_data["items"].append(item)
                print(f"      ✅ Item {j}: {item.get('title')} = {item.get('value')}")
        
        return month_data
    
    def _process_item(self, block: dict, level: int = 0) -> dict | None:
        block_type = block.get("type")
        
        if block_type != "to_do":
            return None
        
        text = self.parser.extract_text(block)
        if not text or not text.strip():
            return None
        
        title, value = self.parser.split_title_value(text)
        
        item = {
            "title": title,
            "value": value
        }
        
        children = block.get("children", [])
        if children:
            sub_items = []
            for child in children:
                if child.get("type") in ["divider", "paragraph"]:
                    continue
                    
                sub_item = self._process_item(child, level + 1)
                if sub_item:
                    sub_items.append(sub_item)
            
            if sub_items:
                item["children"] = sub_items
        
        return item
    
    def _month_code_to_name(self, code: str) -> str:
        months = {
            "01": "Janeiro", "02": "Fevereiro", "03": "Março",
            "04": "Abril", "05": "Maio", "06": "Junho",
            "07": "Julho", "08": "Agosto", "09": "Setembro",
            "10": "Outubro", "11": "Novembro", "12": "Dezembro"
        }
        
        if "/" in code:
            month_num = code.split("/")[0]
            return months.get(month_num, "")
        
        return ""
    
    def _process_summary(self, blocks: list) -> dict:
        summary = {
            "title": "Resumo até o final do Ano",
            "items": []
        }
        
        try:
            print("\n📊 Procurando bloco de resumo...")
            
            found_summary = False
            for i, block in enumerate(blocks):
                block_type = block.get("type")
                text = self.parser.extract_text(block)
                
                if block_type in ["heading_2", "heading_3"]:
                    if "Resumo" in text or "resumo" in text:
                        print(f"   ✅ Resumo encontrado no bloco {i}: '{text}'")
                        found_summary = True
                        
                        if text.strip():
                            summary["title"] = text.replace("🚀", "").strip()
                        continue
                
                if found_summary and block_type == "to_do":
                    item = self._process_item(block)
                    if item:
                        summary["items"].append(item)
                        print(f"      ✅ Item do resumo: {item.get('title')} = {item.get('value')}")
                
                elif found_summary and block_type in ["heading_1", "heading_2", "heading_3", "child_page"]:
                    if "Resumo" not in text and "resumo" not in text:
                        print(f"   🛑 Fim do resumo detectado no bloco {i}")
                        break
            
            if not found_summary:
                print("   ⚠️ Bloco de resumo não encontrado")
            
        except Exception as e:
            print(f"   ❌ ERRO ao processar resumo: {e}")
            import traceback
            traceback.print_exc()
        
        return summary