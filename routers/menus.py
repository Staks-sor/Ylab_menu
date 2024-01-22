from data.config import BASE_URL
from db.database import DataBase
from db.models import MenuModel
from fastapi import APIRouter, status

# Создание экземпляра APIRouter
menus = APIRouter()

# Создание экземпляра базы данных
db = DataBase()

# Формирование URL для запросов
base_url = BASE_URL + "/menus"

# Получение всех меню
@menus.get(base_url)
async def menus_get():
    """
    Получение всех меню
    """
    # Получение данных из базы данных
    data = await db.menus.get_all()
    return data


# Добавление нового меню
@menus.post(base_url)
async def menus_post(menu_model: MenuModel):
    """
    Добавление нового меню
    """
    # Вставка модели меню в базу данных
    await db.menus.insert(menu_model)
    return menu_model


# Получение информации о конкретном меню
@menus.get(base_url+"/{_id}")
async def menus_get_id(_id: int):
    """
    Получение информации о конкретном меню
    """
    # Получение данных из базы данных по указанному ID
    data = await db.menus.get_id(_id)
    return data


# Обновление информации о конкретном меню
@menus.patch(base_url+"/{_id}")
async def menus_patch_id(_id: int, menu_model: MenuModel):
    """
    Обновление информации о конкретном меню
    """
    # Установка ID модели меню
    menu_model.id = _id
    # Обновление данных в базе данных
    await db.menus.update(menu_model)
    return menu_model


# Удаление конкретного меню
@menus.delete(base_url+"/{_id}")
async def menus_delete_id(_id: int):
    """
    Удаление конкретного меню
    """
    # Удаление данных из базы данных по указанному ID
    await db.menus.delete(_id)
    return status.HTTP_200_OK
