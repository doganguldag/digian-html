
from flask import Flask, flash, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_admin import Admin
from os import path
from flask_babel import Babel


# Uygulama ve Veritabanı Yapılandırması
app = Flask(__name__)
babel = Babel(app)
basedir = path.abspath(path.dirname(__file__))
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + path.join(basedir, 'site.db')


# Uygulama Eklentileri
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.init_app(app)
from app.my_admin.routes import MyAdminIndexView
admin = Admin(app, name='Admin', index_view=MyAdminIndexView(), template_mode='bootstrap3')

# Model ve View İçe Aktarmaları
from app.models import Customer, Messages, Newsletter, Quote, Service, User,Messages
from flask_admin.contrib.sqla import ModelView
from app.auth import auth as auth_blueprint

class QuoteAdmin(ModelView):
    column_list = ('id', 'user', 'service', 'request_date')  # user_id ve service_id'yi ekleyin


# Admin Paneli
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Service, db.session))
admin.add_view(ModelView(Newsletter, db.session))
admin.add_view(ModelView(Messages, db.session))
admin.add_view(ModelView(Customer, db.session))
admin.add_view(QuoteAdmin(Quote, db.session))


app.register_blueprint(auth_blueprint, url_prefix='/auth')

from app import views, models
from app.models import User

from app import app, db
from app.models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_request
def before_request():
    if "/admin" in request.url:
        if current_user.is_authenticated and current_user.is_admin:
            return None
        else:
            return redirect(url_for("auth.login"))
        
        
