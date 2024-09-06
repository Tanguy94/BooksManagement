# Utiliser une image Python
FROM python:3.9
 
# Définir le répertoire de travail dans le conteneur
WORKDIR /app
 
# Copier le fichier requirements.txt (que nous allons créer) et installer les dépendances
COPY requirements.txt .
RUN pip install -r requirements.txt
 
# Copier tout le contenu du projet dans le répertoire de travail
COPY . .
 
# Exposer le port 8000 (le port par défaut utilisé par Uvicorn)
EXPOSE 8000
 
# Démarrer l'application avec Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
