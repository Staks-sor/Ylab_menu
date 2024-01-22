from data.config import BASE_URL
from db.database import DataBase
from db.models import SubMenuModel
from fastapi import APIRouter, status

# Создание экземпляра APIRouter
submenus = APIRouter()

# Создание экземпляра базы данных
db = DataBase()

# Формирование URL для запросов
base_url = BASE_URL + "/menus/{menu_id}/submenus"

# Получение всех подменю для определенного меню
@submenus.get(base_url)
async def submenus_get(menu_id: int):
    """
    Получение всех подменю для определенного меню
    """
    data = await db.submenus.get_all(menu_id)
    return data


# Создание нового подменю для определенного меню
@submenus.post(base_url)
async def submenus_post(menu_id: int, submenu_model: SubMenuModel):
    """
    Создание нового подменю для определенного меню
    """
    submenu_model.menu_id = menu_id
    await db.submenus.insert(submenu_model)
    return submenu_model


# Получение информации о конкретном подменю
@submenus.get(base_url+"/{_id}")
async def submenus_get_id(_id: int):
    """
    Получение информации о конкретном подменю
    """
    data = await db.submenus.get_id(_id)
    return data


# Обновление информации о конкретном подменю
@submenus.patch(base_url+"/{_id}")
async def submenus_patch_id(menu_id: int, _id: int, submenu_model: SubMenuModel):
    """
    Обновление информации о конкретном подменю
    """
    submenu_model.menu_id = menu_id
    submenu_model.id = _id
    await db.submenus.update(submenu_model)
    return submenu_model


# Удаление конкретного подменю
@submenus.delete(base_url+"/{_id}")
async def submenus_delete_id(_id: int):
    """
    Удаление конкретного подменю
    """
    await db.submenus.delete(_id)
    return status.HTTP_200_OK
