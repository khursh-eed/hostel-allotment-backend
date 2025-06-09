from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate 
import os


db = SQLAlchemy()
# *******
# # flask setup 
# login_manager = LoginManager()
# login_manager.login_view = 'auth.login'

# if someone tries to access a protected page, redirect them to this login route. auth.login means login function in auth folder

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'super-secret-key'  # change later
    # protects data
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:Khursh%402005@127.0.0.1:3306/hostel_system"

    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'app', 'static', 'uploads')


    # flask setup 
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'


    # linkign the db, login manager and stuff
    
    db.init_app(app)
    login_manager.init_app(app)
    Migrate(app, db)


    # Import User model here (after db is initialized)
    from .models import User

    # Register user_loader callback
    # to search if user logged in
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint
    from .admin import admin as admin_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/')
    app.register_blueprint(main_blueprint, url_prefix='/')
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    
    # print("Blueprints registered:", app.blueprints.keys())


    

    return app


