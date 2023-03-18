from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import smtplib
from datetime import datetime


app = Flask(__name__)
app.config['MYSQL_HOST'] = '3306'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '####'
app.config['MYSQL_DB'] = 'first_project'
mysql = MySQL(app)


class Email:
    def __init__(self, recipient, subject, body, sent_at=None):
        self.recipient = recipient
        self.subject = subject
        self.body = body
        self.sent_at = sent_at


@app.route('/email/send', methods=['POST'])
def send_email():
    recipient = request.json.get('recipient')
    subject = request.json.get('subject')
    body = request.json.get('body')
    sender = 'sivamula.game03@gmail.com'
    password = '####'
    message = f'Subject: {subject}\n\n{body}'

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, recipient, message)
        sent_at = datetime.now()
        email = Email(recipient=recipient, subject=subject, body=body, sent_at=sent_at)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO email (recipient, subject, body, sent_at) VALUES (%s, %s, %s, %s)", (recipient, subject, body, sent_at))
        mysql.connection.commit()
        cur.close()

    return 'Email sent successfully'


if __name__ == '__main__':
    app.run(port=8080, debug=True)

