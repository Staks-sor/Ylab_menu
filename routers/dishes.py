from data.config import BASE_URL
from db.database import DataBase
from db.models import DishModel
from fastapi import APIRouter, status

dishes = APIRouter()
db = DataBase()
base_url = BASE_URL + "/menus/{menu_id}/submenus/{submenu_id}/dishes"


@dishes.get(base_url)
async def dishes_get(submenu_id: int):
    # Обработчик GET-запроса для получения списка блюд
    # Принимает параметр submenu_id типа int из пути запроса
    data = await db.dishes.get_all(submenu_id)
    return data


@dishes.post(base_url)
async def dishes_post(submenu_id: int, dishes_model: DishModel):
    # Обработчик POST-запроса для создания блюда
    # Принимает параметры submenu_id типа int и dishes_model типа DishModel из пути запроса и тела запроса соответственно
    dishes_model.submenu_id = submenu_id
    await db.dishes.insert(dishes_model)
    return dishes_model


@dishes.get(base_url + "/{_id}")
async def dishes_get_id(_id: int):
    # Обработчик GET-запроса для получения конкретного блюда по его идентификатору
    # Принимает параметр _id типа int из пути запроса
    data = await db.dishes.get_id(_id)
    return data


@dishes.patch(base_url + "/{_id}")
async def dishes_patch_id(submenu_id: int, _id: int, dishes_model: DishModel):
    # Обработчик PATCH-запроса для обновления конкретного блюда
    # Принимает параметры submenu_id типа int, _id типа int и dishes_model типа DishModel из пути запроса, пути запроса и тела запроса соответственно
    dishes_model.submenu_id = submenu_id
    dishes_model.id = _id
    await db.dishes.update(dishes_model)
    return dishes_model


@dishes.delete(base_url + "/{_id}")
async def dishes_delete_id(_id: int):
    # Обработчик DELETE-запроса для удаления конкретного блюда
    # Принимает параметр _id типа int из пути запроса
    await db.dishes.delete(_id)
    return status.HTTP_200_OK
