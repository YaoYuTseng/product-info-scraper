from dataclasses import dataclass
from typing import Optional


@dataclass
class Product:
    category: Optional[str] = None
    model: Optional[str] = None
    title: Optional[str] = None
    highlight: Optional[str] = None
    description: Optional[str] = None
