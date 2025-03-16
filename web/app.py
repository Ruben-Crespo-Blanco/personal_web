from flask import Flask, render_template, flash, redirect, request
from flask_mail import Mail, Message
import os
from config import Config




def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = Config.SECRET_KEY
    app.config['MAIL_SERVER'] = Config.MAIL_SERVER            
    app.config['MAIL_PORT'] = Config.MAIL_PORT
    app.config['MAIL_USE_TLS'] = Config.MAIL_USE_TLS
    app.config['MAIL_USERNAME'] = Config.MAIL_USERNAME    
    app.config['MAIL_PASSWORD'] = Config.MAIL_PASSWORD       
    app.config['MAIL_DEFAULT_SENDER'] = Config.MAIL_DEFAULT_SENDER

    mail = Mail(app)

    @app.route('/')
    def hello():
        return render_template("index.html")
    

    @app.route('/contact', methods=['POST'])
    def contact():
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Compose the email
        msg = Message(subject=f"New Contact Message from {name}",
                    recipients=['rcresb@gmail.com'],  # Where to send the message
                    body=f"From: {name} <{email}>\n\nMessage:\n{message}")
    
        try:
            mail.send(msg)
            flash('Message sent successfully!', 'success')
        except Exception as e:
            print(f"Error sending email: {e}")
            flash('Failed to send message. Please try again later.', 'error')

        return redirect('/')
    
    return app







if __name__ == "__main__":
    create_app().run()