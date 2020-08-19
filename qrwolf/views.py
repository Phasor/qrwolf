from qrwolf import app
from datetime import datetime
from flask import render_template, request, redirect, session, url_for, Response, make_response
from flask_mail import Mail, Message

@app.route('/', methods=["GET","POST"])
def home():

    if request.method == "POST":

        req = request.form
        query_url = req["url"]
        #print(query_url)
        #return redirect(
        #'result.html',
        #query_url)


    return render_template('index.html',title='QR Code Scanner: create a QR code now', 
           description='Use our free QR code generator to drive traffic to your website, send SMS, emails and more.')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html', title ="Contact QR Wolf")

@app.route('/how-to-use-qr-codes')
def tutorial():
    return render_template('tutorial.html', title="QR Code FAQ")


@app.route('/qr-code', methods=["GET","POST"])
@app.route('/qr-code/<code_size>', methods=["GET","POST"])
def result(code_size=None):
    if request.method == 'POST':

        req = request.form
        requested_url = req["url"]
        code_type = req["radiogrp"] #get the type of code e.g. URL/phone/email etc
        
        #update code based on type of code asked for
        if code_type == "email":
            prepend = "mailto:"
            requested_url = prepend + requested_url

        if code_type == "phone":
            prepend = "tel:"
            requested_url = prepend + requested_url
        
        if code_type == "sms":
            prepend = "sms:"
            requested_url = prepend + requested_url
        
        if code_type == "geo":
            prepend = "geo:"
            requested_url = prepend + requested_url

        base_url = "https://chart.googleapis.com/chart?chs=200x200&cht=qr&chl="   
        query_url = base_url + requested_url
        session['query_url'] = query_url #insert into session
        session['requested_url'] = requested_url #insert into session

        return render_template('generate.html', query_url=query_url, title='Here is your free QR code', description='Here you can see your QR code')

    else: #user has asked to resize the code, hence URL is in session already
        
        requested_url = session.get('requested_url', None) #get url the user wants
         
        if code_size == 'small':
            base_url = "https://chart.googleapis.com/chart?chs=75x75&cht=qr&chl="
        elif code_size == 'medium':
            base_url = "https://chart.googleapis.com/chart?chs=150x150&cht=qr&chl="
        else:
            base_url = "https://chart.googleapis.com/chart?chs=250x250&cht=qr&chl="
        
        query_url = base_url + requested_url
        session['query_url'] = query_url #update session

        return render_template('generate.html', query_url=query_url,title='Here is your free QR code', description='Here you can see your QR code')


@app.route('/success', methods=["GET","POST"])
def get_success():
    
    if request.method == "POST":
        req = request.form
        email = req["email_address"]
        code = session.get('query_url', None)
        msg = Message( subject="Here is your QR Wolf QR code", sender='admin@qrwolf.com', recipients=[email,'admin@qrwolf.com'] )
        msg.html = render_template('email.html', code_url = code)
        mail = Mail(app)
        mail.send(msg)

        return render_template('generate.html', query_url = code, status_msg="Your code has been sent!", show_link=True)

    return render_template('generate.html', query_url = code, status_msg="Something went wrong.")

@app.route('/sitemap.xml')
def sitemap():
    lastmod = datetime.now()
    lastmod = lastmod.strftime('%Y-%m-%d')
    
    pages = [
        ['http://www.qrwolf.com', lastmod],
        ['http://www.qrwolf.com/how-to-use-qr-codes', lastmod],
        ['http://www.qrwolf.com/about', lastmod],
        ['http://www.qrwolf.com/contact',lastmod]
    ]

    sitemap_template = render_template('sitemap.xml', pages=pages)
    response = make_response(sitemap_template)
    response.headers['Content-Type'] = 'application/xml'
    return response


    

