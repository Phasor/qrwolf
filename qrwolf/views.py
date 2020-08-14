from qrwolf import app
from datetime import datetime
from flask import render_template, request, redirect, session
from flask_mail import Mail, Message

@app.route('/', methods=["GET","POST"])
def home():

    if request.method == "POST":

        req = request.form
        query_url = req["url"]
        print(query_url)
        #return redirect(
        #'result.html',
        #query_url)


    return render_template('index.html',title='Free QR Code Generator: create a QR code now', 
           description='Use our free QR code generator to drive more traffic to your site.')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html', title ="QuikQR: Contact us")

@app.route('/how-to-use-qr-codes')
def tutorial():
    return render_template('tutorial.html')


@app.route('/qr-code', methods=["GET","POST"])
@app.route('/qr-code/<code_size>', methods=["GET","POST"])
def result(code_size=None):
    if request.method == 'POST':

        req = request.form
        requested_url = req["url"]
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
        msg = Message(subject="Here is your QuikQR QR code", sender='admin@benmurison.com', recipients=[email])
        msg.html = render_template('email.html', code_url = code)
        mail = Mail(app)
        mail.send(msg)

        return render_template('generate.html', query_url = code, status_msg="Your code has been sent!", show_link=True)

    return render_template('generate.html', query_url = code, status_msg="Something went wrong.")



