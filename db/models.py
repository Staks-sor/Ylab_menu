from decimal import Decimal
from typing import Optional, Tuple

from pydantic import BaseModel


class DishModel(BaseModel):
    id: Optional[int] = None
    submenu_id: Optional[int] = None
    title: str
    description: str
    price: Decimal

    def to_tuple(self) -> Tuple:
        return (
            self.id,
            self.submenu_id,
            self.title,
            self.description,
            self.price
        )


class SubMenuModel(BaseModel):
    id: Optional[int] = None
    menu_id: Optional[int] = None
    title: str
    description: str
    dishes_count: Optional[int] = 0

    def to_tuple(self) -> Tuple:
        return (
            self.id,
            self.menu_id,
            self.title,
            self.description
        )


class MenuModel(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    submenus_count: Optional[int] = 0

    def to_tuple(self) -> Tuple:
        return (
            self.id,
            self.title,
            self.description
        )
