class NotionParser:
    
    @staticmethod
    def extract_text(block: dict) -> str:
        try:
            block_type = block.get("type")

            if not block_type:
                return ""
            
            content = block.get(block_type, {})

            if "rich_text" in content:
                return NotionParser._extract_from_rich_text(content.get("rich_text", []))

            if "title" in content:
                return NotionParser._extract_from_rich_text(content.get("title", []))

            if "text" in content:
                text_content = content.get("text", {})

                if isinstance(text_content, dict):
                    return text_content.get("content", "")
                
                elif isinstance(text_content, str):
                    return text_content
            
            return ""
            
        except Exception as e:
            print(f"⚠️ Erro ao extrair texto do bloco: {e}")
            return ""
    
    @staticmethod
    def _extract_from_rich_text(items: list) -> str:
        text_parts = []
        
        for item in items:
            try:
                if isinstance(item, dict):

                    if "plain_text" in item:
                        text_parts.append(item.get("plain_text", ""))

                    elif "text" in item:
                        text_obj = item.get("text", {})

                        if isinstance(text_obj, dict):
                            text_parts.append(text_obj.get("content", ""))

                        elif isinstance(text_obj, str):
                            text_parts.append(text_obj)

                elif isinstance(item, str):
                    text_parts.append(item)

            except Exception as e:
                print(f"⚠️ Erro ao processar item: {e}")
                continue
        
        return "".join(text_parts)
    
    @staticmethod
    def extract_checkbox_state(block: dict) -> bool:
        try:
            block_type = block.get("type")

            if block_type == "to_do":
                return block.get("to_do", {}).get("checked", False)
            return False
        
        except:
            return False
    
    @staticmethod
    def split_title_value(text: str) -> tuple[str, str]:
        try:
            if ":" in text:
                parts = text.split(":", 1)
                return parts[0].strip(), parts[1].strip()
            return text.strip(), ""
        
        except:
            return text if isinstance(text, str) else "", ""