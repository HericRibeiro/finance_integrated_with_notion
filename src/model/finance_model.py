from pydantic import BaseModel
from typing import List, Optional


class FinanceSubItem(BaseModel):
    title: str
    value: str
    sub_items: Optional[List['FinanceSubItem']] = None


class FinanceItem(BaseModel):
    title: str
    value: str
    sub_items: Optional[List[FinanceSubItem]] = None


class MonthData(BaseModel):
    month: str
    code: str
    items: List[FinanceItem]


class SummaryData(BaseModel):
    title: str
    items: List[FinanceItem]


class FinanceResponse(BaseModel):
    months: List[MonthData]
    summary: SummaryData


FinanceSubItem.model_rebuild()