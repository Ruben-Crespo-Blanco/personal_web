from flask import Flask, render_template, flash, redirect, request
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv


load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = os.getenv("SECRET_KEY")
    app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")            
    app.config['MAIL_PORT'] = os.getenv("MAIL_PORT")
    app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS")
    app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")    
    app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")       
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER")

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
    app = create_app()
    app.run(debug=True)