import sqlite3
from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
from typing import List, Optional
 
app = FastAPI()
 
# Connexion à la base de données SQLite
DATABASE = "library.db"
 
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Pour avoir les résultats sous forme de dictionnaire
    return conn
 
# Clé API statique pour l'exemple
API_KEY = '123456789ABC'
 
# Vérification de la clé API
async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Clé API invalide")
 
# Modèle pour les livres
class BookCreate(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    year: int
 
# Créer la table "books" dans SQLite si elle n'existe pas
def create_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            description TEXT,
            year INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
 
create_table()  # Appel lors du démarrage pour s'assurer que la table existe
 
# Endpoint pour recevoir un body JSON avec les livres du groupe 1 (requiert la clé API)
@app.post("/upload-books-json/", dependencies=[Depends(verify_api_key)])
async def upload_books_json(books_data: List[BookCreate]):
    # Connexion à la base de données
    conn = get_db_connection()
    cursor = conn.cursor()
 
    # Parcourir chaque livre dans le body JSON et l'ajouter à la base de données
    for book in books_data:
        cursor.execute('''
            INSERT INTO books (title, author, description, year)
            VALUES (?, ?, ?, ?)
        ''', (book.title, book.author, book.description, book.year))
 
    conn.commit()
    conn.close()
 
    return {"status": "Books added successfully", "total_books": len(books_data)}
 
# Endpoint pour obtenir la liste de tous les livres (pas besoin de clé API)
@app.get("/books", response_model=List[BookCreate])
def get_books():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return [dict(book) for book in books]