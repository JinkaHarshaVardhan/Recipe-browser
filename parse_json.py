import json
import sqlite3

# Load JSON data
with open("c:/Users/Harsha vardhan/Downloads/US_recipes_null.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# print(json.dumps(data))
# Connect to SQLite database
conn = sqlite3.connect("recipes.db")
cur = conn.cursor()

# Create table
cur.execute("""
CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    cuisine TEXT,
    country TEXT,
    rating REAL,
    total_time INTEGER,
    prep_time INTEGER,
    cook_time INTEGER,
    description TEXT,
    ingredients TEXT,
    instructions TEXT,
    nutrients TEXT,
    serves TEXT,
    url TEXT
)
""")

# Insert data
for _, recipe in data.items():
    cur.execute("""
    INSERT INTO recipes (title, cuisine, country, rating, total_time, prep_time, cook_time,
                         description, ingredients, instructions, nutrients, serves, url)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        recipe.get("title"),
        recipe.get("cuisine"),
        recipe.get("Country_State"),
        recipe.get("rating"),
        recipe.get("total_time"),
        recipe.get("prep_time"),
        recipe.get("cook_time"),
        recipe.get("description"),
        json.dumps(recipe.get("ingredients")),
        json.dumps(recipe.get("instructions")),
        json.dumps(recipe.get("nutrients")),
        recipe.get("serves"),
        recipe.get("URL")
    ))

conn.commit()
conn.close()
print("Data successfully stored in recipes.db")