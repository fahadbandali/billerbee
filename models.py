from pydantic import BaseModel
from typing import List, Optional

class InvoiceEntry(BaseModel):
    Item: str
    Business: str
    Address: str
    Date: str
    PaymentType: Optional[str]
    Card_Id: Optional[str]
    Quantity: int
    Price: float
    Tax: float
    Total: float
    
class Invoice(BaseModel):
    entries: List[InvoiceEntry]
