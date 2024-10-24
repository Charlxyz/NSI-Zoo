from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
from utils import login_required, admin_required, soigneur_required

app = Flask(__name__, template_folder="./templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bdd.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '\xf0?a\x9a\\\xff\xd4;\x0c\xcbHi'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

@login_manager.user_loader # Charge l'utilisateur si il se connecte
def load_user(id):
    return User.query.get(int(id))

class User(db.Model, UserMixin): # Définir le modèle User
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False) # user, soigneur, admin

    def __repr__(self):
        return f'<User {self.username}>'

class Animaux(db.Model): # Définir le modèle Animaux
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80), unique=True, nullable=False)
    race = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    soin = db.Column(db.String(200), nullable=True)
    soigneur = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Animaux {self.nom}>'

class Soigneur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80), nullable=False)

@app.route('/') # Page d'acceuil
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/acceuil-soigneur')
@soigneur_required
def acceuil_soigneur():
    animaux = Animaux.query.all()
    return render_template("acceuil_soigneur.html", animaux=animaux)

@app.route('/login', methods=['POST', 'GET']) # Page de connexion
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            email = request.form['email'] # Récupere l'email inscrit dans le html
            password = request.form['password'] # Récupere le mot de passe inscrit dans le html
            if all(value not in ["", None, " "] for value in [email, password]):
                user = User.query.filter_by(email=email).first() # Verrifie l'existance de l'adresse mail dans la base de donnee
                if user and bcrypt.check_password_hash(user.password, password): # check_password_hash() permet de comparé le mot de passe dans la base de donnees et celui rentre dans le html
                    login_user(user) # Connecte l'utilisateur on peut rajouter remember=True pour le garder connecter meme si il ferme son navigateur
                    flash("Connexion réussie !", 'success')
                    if current_user.role == 'soigneur':
                        return redirect(url_for('acceuil_soigneur'))
                    elif current_user.role == 'admin':
                        return redirect(url_for('admin'))
                    else:
                        return redirect(url_for('index')) # Redirige a la fonction index
                else:
                    flash('Identifiants incorrects', 'danger')
            else:
                flash("Des informations sont manquantes.", 'danger')

    return render_template("./auth/login.html")

@app.route('/register', methods=['POST', 'GET']) # Page d'inscription
def register():
    if current_user.is_authenticated:
        flash("Vous etes deja connecter", "default")
        return redirect(url_for('index'))
    else:
        if request.method == "POST":
            username = request.form['username'] # Récupere le nom d'utilisateur inscrit dans le html
            email = request.form['email'] # Récupere l'email inscrit dans le html
            password = request.form['password'] # Récupere le mot de passe inscrit dans le html
            check_password = request.form['passwordcheck'] # Récupere le le deuxieme mot de passe inscrit dans le html

            username_exists = User.query.filter_by(username=username).first() # Verrifie si le nom d'utlisateur existe deja
            email_exists = User.query.filter_by(email=email).first() # Verrifie si l'adresse mail existe deja
            
            if username_exists:
                flash(f"{username} est dejà utiliser.", 'danger')
            elif email_exists:
                flash(f"{email} est dejà utiliser.", 'danger')
            elif password != check_password: # Verrifie si les deux mot de passe rentrés sont identiques
                flash("Les mots de passe ne sont pas identiques.", 'danger')
            else:
                if all(value not in ["", None, " "] for value in [username, email, password]):
                    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') # Hash le mot de passe de l'utilisateur pour le rendre indécriptable
                    user = User(
                        username=username,
                        email=email,
                        password=hashed_password,
                        role='user'
                        )
                    db.session.add(user) # Ajoute l'utilisateur a la base de donnes bdd.bd
                    db.session.commit()
                    flash("Compte créé. Veuillez vous connecter.", 'success')
                    return redirect(url_for('login'))
                
                flash("Des informations sont manquantes.", 'danger')

            return redirect(url_for('register'))
    
    return render_template("./auth/register.html")

@app.route('/logout') # Permet de déconnecter l'utilisateur
def logout():
    logout_user()
    flash("Déconnexion réussie !", 'success')
    return redirect(url_for('index'))

@app.route('/admin') # Page de la gestion d'utilisateur et des animaux
@admin_required
def admin():
    return render_template("./admin/admin.html")

# Création des tables de la base de donnee
with app.app_context():
    db.create_all()  # Crée les tables si elles n'existent pas
app.run(debug=True) # Lance le site web
