from flask import Flask, request, jsonify, abort
import sqlite3
 
app = Flask(__name__)
 
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
        
def add_book(title, author, description, year, quantity):
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO books (title, author, description, year, quantity)
        VALUES (?, ?, ?, ?, ?)
    ''', (title, author, description, year, quantity))
    conn.commit()
    conn.close()
    print(f"Livre '{title}' ajouté avec succès !") 
 
 
# Endpoint pour ajouter des livres à la base de données
@app.route('/bookspost/', methods=['POST'])
def bookspost():
    verify_api_key()  # Vérifie la clé API
 
    data = request.get_json()
    title = data['title']
    author = data['author']
    description = data.get('description', '')
    year = data['year']
    quantity = data['quantity']
 
    # Ajouter le livre dans la base de données
    add_book(title, author, description, year, quantity)
 
    return jsonify({"status": f"Livre '{title}' ajouté avec succès !"}),201
 
 

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