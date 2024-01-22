from typing import Dict, Tuple, List, Optional

from data.config import DB_URL
from db.queries import *
from db.models import (
    MenuModel,
    SubMenuModel,
    DishModel
)

import asyncpg


class DBConnect:

    @staticmethod
    async def _fetchone(query: str, params: Optional[Tuple] = None) -> asyncpg.Record:
        conn: asyncpg.Connection = await asyncpg.connect(DB_URL)
        if params:
            data = await conn.fetchrow(query, *params)
        else:
            data = await conn.fetchrow(query)
        await conn.close()
        return data

    @staticmethod
    async def _fetchall(query: str, params: Optional[Tuple] = None) -> List[asyncpg.Record]:
        conn: asyncpg.Connection = await asyncpg.connect(DB_URL)
        if params:
            data = await conn.fetch(query, *params)
        else:
            data = await conn.fetch(query)
        await conn.close()
        return data

    @staticmethod
    async def _change(query: str, params: Optional[Tuple] = None) -> None:
        conn: asyncpg.Connection = await asyncpg.connect(DB_URL)
        if params:
            await conn.execute(query, *params)
        else:
            await conn.execute(query)
        await conn.close()

    async def setup(self) -> None:
        await self._change(CREATE_MENUS_TABLE)
        await self._change(CREATE_SUBMENUS_TABLE)
        await self._change(CREATE_DISHES_TABLE)


class Menus(DBConnect):
    cache: Dict[int, MenuModel] = {}

    async def get_id(self, _id: int) -> MenuModel | None:
        if _id in self.cache:
            return self.cache[_id]
        data = await self._fetchone(MENU_FETCH_ID, (_id,))
        _m = MenuModel(**data)
        submenus_count = await self._fetchone(MENU_SUBMENUS_COUNT, (_m.id,))
        _m.submenus_count = submenus_count[0] or 0
        if _m:
            self.cache[_id] = _m
        return _m

    async def get_all(self) -> List[MenuModel] | None:
        data = await self._fetchall(MENU_FETCH_ALL)
        _ms = []
        for menu in data:
            _m = MenuModel(**menu)
            submenus_count = await self._fetchone(MENU_SUBMENUS_COUNT, (_m.id,))
            _m.submenus_count = submenus_count[0] or 0
            self.cache[_m.id] = _m
            _ms.append(_m)
        return _ms if _ms != [] else None

    async def insert(self, menu_model: MenuModel) -> None:
        await self._change(MENU_INSERT, (*menu_model.to_tuple()[1:],))

    async def update(self, menu_model: MenuModel) -> None:
        await self._change(MENU_UPDATE_ID, (*menu_model.to_tuple(),))
        self.cache[menu_model.id] = menu_model

    async def delete(self, _id: int) -> None:
        await self._change(MENU_DELETE_ID, (_id,))
        if _id in self.cache:
            self.cache.pop(_id)


class SubMenus(DBConnect):
    cache: Dict[int, SubMenuModel] = {}

    async def get_id(self, _id: int) -> SubMenuModel | None:
        if _id in self.cache:
            return self.cache[_id]
        data = await self._fetchone(SUBMENU_FETCH_ID, (_id,))
        _sm = SubMenuModel(**data)
        if _id:
            self.cache[_id] = _sm
        return _sm

    async def get_all(self, _id: int) -> List[SubMenuModel] | None:
        data = await self._fetchall(SUBMENU_FETCH_MENU_ID, (_id,))
        _sms = []
        for submenu in data:
            _sm = SubMenuModel(**submenu)
            self.cache[_sm.id] = _sm
            _sms.append(_sm)
        return _sms if _sms != [] else None

    async def insert(self, submenu_model: SubMenuModel) -> None:
        await self._change(SUBMENU_INSERT, (*submenu_model.to_tuple()[1:],))

    async def update(self, submenu_model: SubMenuModel) -> None:
        await self._change(SUBMENU_UPDATE_ID, (*submenu_model.to_tuple(),))
        self.cache[submenu_model.id] = submenu_model

    async def delete(self, _id: int) -> None:
        await self._change(SUBMENU_DELETE_ID, (_id,))
        if _id in self.cache:
            self.cache.pop(_id)


class Dishes(DBConnect):
    cache: Dict[int, DishModel] = {}

    async def get_id(self, _id: int) -> DishModel | None:
        if _id in self.cache:
            return self.cache[_id]
        data = await self._fetchone(DISHES_FETCH_ID, (_id,))
        _d = DishModel(**data)
        if _d:
            self.cache[_id] = _d
        return _d

    async def get_all(self, _id: int) -> List[DishModel] | None:
        data = await self._fetchall(DISHES_FETCH_SUBMENU_ID, (_id,))
        _ds = []
        for dish in data:
            _d = DishModel(**dish)
            self.cache[_d.id] = _d
            _ds.append(_d)
        return _ds if _ds != [] else None

    async def insert(self, dishes_model: DishModel) -> None:
        await self._change(DISHES_INSERT, (*dishes_model.to_tuple()[1:],))

    async def update(self, dishes_model: DishModel) -> None:
        await self._change(DISHES_UPDATE_ID, (*dishes_model.to_tuple(),))
        self.cache[dishes_model.id] = dishes_model

    async def delete(self, _id: int) -> None:
        await self._change(DISHES_DELETE_ID, (_id,))
        if _id in self.cache:
            self.cache.pop(_id)


class DataBase:
    connection: DBConnect = DBConnect()
    menus: Menus = Menus()
    submenus: SubMenus = SubMenus()
    dishes: Dishes = Dishes()
