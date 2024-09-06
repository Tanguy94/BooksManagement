from flask import Flask, request, jsonify, abort
import sqlite3
 
from flask import Flask
 
app = Flask(__name__)
 
@app.route('/')
def hello():
    return 'Hello, Flask!'

 
# Clé API statique pour l'exemple
API_KEY = "123456789ABC"
 
# Connexion à la base de données SQLite
DATABASE = "library.db"
 
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Pour avoir les résultats sous forme de dictionnaire
    return conn
 
# Créer la table "books" dans SQLite si elle n'existe pas
def create_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            description TEXT,
            year INTEGER NOT NULL,
            quantity INTEGER NOT NULL  -- Ajout de la colonne quantity
        )
    ''')
    conn.commit()
    conn.close()
 
# Vérification de la clé API
def verify_api_key():
    api_key = request.headers.get('x-api-key')
    if api_key != API_KEY:
        abort(403, description="Clé API invalide")

# Endpoint pour obtenir la liste de tous les livres
@app.route('/books', methods=['GET'])
def get_books():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
 
    books_list = [dict(book) for book in books]
    return jsonify(books_list)
 
# Démarrer l'application Flask
if __name__ == '__main__':
    app.run(debug=True)