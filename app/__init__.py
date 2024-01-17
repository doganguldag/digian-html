from flask import Flask, flash, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
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
from app.models import Customer, Messages, Newsletter, Service, User
from app.my_admin import UserModelView
from flask_admin.contrib.sqla import ModelView
from app.auth import auth as auth_blueprint

# Admin Paneli
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Service, db.session))
admin.add_view(ModelView(Newsletter, db.session))
admin.add_view(ModelView(Messages, db.session))
admin.add_view(ModelView(Customer, db.session))

app.register_blueprint(auth_blueprint, url_prefix='/auth')

from app import views, models
from app.models import User

from app import app, db
from app.models import User

"""with app.app_context():
    # Uygulama bağlamı içinde işlemler
    user = User.query.filter_by(username="admin").first()
    if user:
        user.set_password("1234567890")
        # Şifre ve diğer ayarlar
        db.session.commit()"""


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/footer', methods=['POST'])
def add_email_to_newsletter():
    if request.method == 'POST':
        email = request.form['email']
        new_email = Newsletter(email=email)
        try:
            db.session.add(new_email)
            db.session.commit()
            flash('Email added to the newsletter successfully!', 'success')
        except:
            db.session.rollback()
            flash('Error adding email to the newsletter!', 'danger')
        finally:
            db.session.close()

    return redirect(url_for('index'))

@app.route('/contact', methods=['POST'])
def add_message():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        subject = request.form['subject']
        message = request.form['message']
        new_message = Messages(name=name, email=email, phone=phone, subject=subject, message=message)
        try:
            db.session.add(new_message)
            db.session.commit()
            flash('Message added to the messages successfully!', 'success')
        except:
            db.session.rollback()
            flash('Error adding message to the messages!', 'danger')
        finally:
            db.session.close()
            
    return redirect(url_for('contact'))

"""@babel.localeselector
def get_locale():
    # Kullanıcıya ait dil tercihini döndürür
    # Örnek: 'en' veya 'de'
    return 'en'"""