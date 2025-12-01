import re
from typing import Tuple


def extract_month_name_from_code(code: str) -> str:
    months = {
        "01": "Janeiro", "02": "Fevereiro", "03": "Março",
        "04": "Abril", "05": "Maio", "06": "Junho",
        "07": "Julho", "08": "Agosto", "09": "Setembro",
        "10": "Outubro", "11": "Novembro", "12": "Dezembro"
    }
    
    match = re.match(r"(\d{2})/(\d{4})", code)
    if match:
        month_num = match.group(1)
        return months.get(month_num, "")
    
    return ""


def format_currency(value: str) -> str:
    cleaned = value.replace(" ", "").replace(".", "").replace(",", ".")
    try:
        num_value = float(cleaned)
        return f"{num_value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return value


def parse_notion_date(date_str: str) -> str:
    return date_str