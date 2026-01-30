from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Modèle de données : Utilisateur
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Création des tables au démarrage (pour simplifier le projet, sans migrations complexes)
with app.app_context():
    try:
        db.create_all()
        print("Base de données initialisée.")
    except Exception as e:
        print(f"Erreur lors de l'initialisation de la DB (normal si pas de connexion lors du build): {e}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        
        if username and email:
            new_user = User(username=username, email=email)
            try:
                db.session.add(new_user)
                db.session.commit()
            except Exception as e:
                return f"Erreur lors de l'ajout: {str(e)}"
            return redirect(url_for('index'))
            
    # Récupération de tous les utilisateurs
    try:
        users = User.query.all()
    except Exception as e:
        users = []
        print(f"Erreur de connexion DB: {e}")
        
    return render_template('index.html', users=users)

@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    # Écoute sur toutes les interfaces pour Docker/Jenkins
    app.run(host='0.0.0.0', port=5000, debug=True)
