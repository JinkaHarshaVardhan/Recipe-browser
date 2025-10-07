from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3

app = FastAPI(title="Recipe API")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_db_connection():
    conn = sqlite3.connect("recipes.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/recipes")
def get_recipes(
    search: str = Query(None),
    sort_by: str = Query("rating"),
    order: str = Query("desc"),
    page: int = Query(1, ge=1),
    per_page: int = Query(5, le=50)
):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM recipes"
    params = []

    if search:
        query += " WHERE title LIKE ? OR cuisine LIKE ?"
        params += [f"%{search}%", f"%{search}%"]

    if sort_by not in ["rating", "total_time", "title"]:
        sort_by = "rating"
    query += f" ORDER BY {sort_by} {'ASC' if order == 'asc' else 'DESC'}"

    offset = (page - 1) * per_page
    query += " LIMIT ? OFFSET ?"
    params += [per_page, offset]

    recipes = cursor.execute(query, params).fetchall()
    conn.close()
    return JSONResponse([dict(row) for row in recipes])