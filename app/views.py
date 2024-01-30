
from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user
from app import app, db
from app.models import Customer, Newsletter, Service, Messages, Quote, User

@app.route('/index.html')
@app.route('/')
def index():
    services = Service.query.all()
    customers = Customer.query.all()
    return render_template('index.html',customers=customers, services=services)

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/casestudy1.html')
def casestudy1():
    return render_template('casestudy1.html')

@app.route('/casestudy2.html')
def casestudy2():
    return render_template('casestudy2.html')


@app.route('/activeservice.html/<servicename>')
def activeservice(servicename):
    services = Service.query.all()
    return render_template('activeservice.html',services = services, servicename = servicename)


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
            
        return render_template('contact.html')
    
    elif request.method == 'GET':
        return render_template('contact.html')
      

@app.route('/service.html')
def service():
    services = Service.query.all()
    return render_template('service.html', services=services)

@app.route('/contact.html')
def contact():
    services = Service.query.all()
    return render_template('contact.html', services=services)

@app.route('/request_quote/<int:service_id>', methods=['POST'])
def request_quote(service_id):
    service = Service.query.get(service_id)

    if current_user.is_authenticated:
        user = current_user  # Assuming you are using Flask-Login for authentication

        # Check if the user has already requested a quote for this service
        existing_quote = Quote.query.filter_by(user_id=user.id, service_id=service.id).first()
        if existing_quote:
            flash('You have already requested a quote for this service.', 'warning')
        else:
            quote = Quote(user=user, service=service)
            db.session.add(quote)
            db.session.commit()
            flash('Quote request submitted successfully.', 'success')
    else:
        flash('You need to be logged in to request a quote.', 'danger')

    return redirect(url_for('service', servicename=service.title))