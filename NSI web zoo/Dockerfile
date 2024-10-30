FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install -r requirements.txt

# Copier le code de l'application
COPY . .

# Exposer le port
EXPOSE 80

# Définir la commande de démarrage
CMD ["python", "main.py"]