from flask import render_template, redirect, url_for, request, flash
from app import app, db
from app.models import Customer, Newsletter, Service

@app.route('/index.html')
@app.route('/')
def index():
    customers = Customer.query.all()
    return render_template('index.html',customers=customers)

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/service.html')
def service():
    return render_template('service.html')

@app.route('/linkbuilding.html')
def linkbuilding():
    return render_template('linkbuilding.html')

@app.route('/activeservice.html/<servicename>')
def activeservice(servicename):
    services = Service.query.all()
    return render_template('activeservice.html',services = services, servicename = servicename)



@app.route('/onmarketing.html')
def onmarketing():
    return render_template('onmarketing.html')









  

  


