import os

# Загрузить переменные окружения из файла .env
with open('.env', 'r') as file:
    for line in file:
        key, value = line.strip().split('=')
        os.environ[key] = value

# Использование переменных окружения
db_usr = os.environ["DB_USER"]
db_pwd = os.environ["DB_PASSWORD"]

DB_URL = f"postgresql://{db_usr}:{db_pwd}@192.168.0.104:5432/ylab"
BASE_URL = "/api/v1"
