# Tables
CREATE_MENUS_TABLE = """
CREATE TABLE IF NOT EXISTS menus (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL
)
"""
CREATE_SUBMENUS_TABLE = """
CREATE TABLE IF NOT EXISTS submenus (
    id SERIAL PRIMARY KEY,
    menu_id INT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    FOREIGN KEY (menu_id) REFERENCES menus (id) ON DELETE CASCADE
)
"""
CREATE_DISHES_TABLE = """
CREATE TABLE IF NOT EXISTS dishes (
    id SERIAL PRIMARY KEY,
    submenu_id INT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    price DECIMAL NOT NULL,
    FOREIGN KEY (submenu_id) REFERENCES submenus (id) ON DELETE CASCADE
)
"""

# Menus
MENU_INSERT = """
INSERT INTO menus(title, description) VALUES($1, $2);
"""
MENU_FETCH_ID = f"""
    SELECT *, 
    (SELECT COUNT(*) FROM submenus WHERE menu_id = $1) AS submenus_count 
    FROM menus WHERE id = $1;
"""
MENU_FETCH_ALL = """SELECT * FROM menus;"""
MENU_UPDATE_ID = """
UPDATE menus 
    SET
        id = $1,
        title = $2,
        description = $3
    WHERE id = $1;
"""
MENU_DELETE_ID = """DELETE FROM menus WHERE id = $1;"""
MENU_SUBMENUS_COUNT = """SELECT COUNT(*) FROM submenus WHERE menu_id = $1;"""

# SubMenus
SUBMENU_INSERT = """
INSERT INTO submenus(menu_id, title, description) VALUES($1, $2, $3)
"""
SUBMENU_FETCH_ID = """
    SELECT *, 
    (SELECT COUNT(*) FROM dishes WHERE submenu_id = $1) AS dishes_count
    FROM submenus WHERE id = $1;
"""
SUBMENU_FETCH_MENU_ID = """SELECT * FROM submenus WHERE menu_id = $1;"""
SUBMENU_UPDATE_ID = """
UPDATE submenus 
    SET
        id = $1,
        menu_id = $2,
        title = $3,
        description = $4
    WHERE id = $1;
"""
SUBMENU_DELETE_ID = """DELETE FROM submenus WHERE id = $1;"""
SUBMENU_DISHES_COUNT = """SELECT COUNT(*) FROM dishes WHERE submenu_id = $1;"""

# Dishes
DISHES_INSERT = """
INSERT INTO dishes (submenu_id, title, description, price) VALUES($1, $2, $3, $4);
"""
DISHES_FETCH_ID = """SELECT * FROM dishes WHERE id = $1;"""
DISHES_FETCH_SUBMENU_ID = """SELECT * FROM dishes WHERE submenu_id = $1;"""
DISHES_UPDATE_ID = """
UPDATE dishes 
    SET
        id = $1,
        submenu_id = $2,
        title = $3,
        description = $4,
        price = $5
    WHERE id = $1;
"""
DISHES_DELETE_ID = """DELETE FROM dishes WHERE id = $1;"""
