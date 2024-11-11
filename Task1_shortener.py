import sqlite3
import string
import random
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

DATABASE_FILE = "shortener.db"

app = FastAPI()


class URLRequest(BaseModel):
    url: str


# Инициализация БД
def init_db():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_id TEXT NOT NULL UNIQUE
        )
    """)
    conn.commit()
    conn.close()


# Генерация уникального short_id длиной length
def generate_short_id(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Получение short_id
def get_short_id():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    # Генерируем новый айдишник до тех пор, пока он не будет уникальным
    while True:
        short_id = generate_short_id()
        cursor.execute("SELECT 1 FROM links WHERE short_id = ?", (short_id,))
        if not cursor.fetchone():
            break

    conn.close()
    return short_id


# Сохранение оригинальной ссылки и short_id в базе данных
def save_link(original_url, short_id):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO links (original_url, short_id) VALUES (?, ?)", (original_url, short_id))
    conn.commit()
    conn.close()


# Получение оригинальной ссылки по short_id
def get_original_url(short_id):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT original_url FROM links WHERE short_id = ?", (short_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


# Эндпоинт для создания короткой ссылки
@app.post("/shorten")
def shorten_url(request: URLRequest):
    original_url = request.url
    short_id = get_short_id()
    save_link(original_url, short_id)
    short_url = f"http://localhost:8000/{short_id}"
    return {"short_url": short_url}


# Эндпоинт для редиректа по короткому URL
@app.get("/{short_id}")
def redirect_to_url(short_id: str):
    original_url = get_original_url(short_id)
    if original_url:
        return RedirectResponse(url=original_url)
    else:
        return {"error": "Short URL not found"}

# Запуск инициализации БД при старте приложения
@app.on_event("startup")
def on_startup():
    init_db()


