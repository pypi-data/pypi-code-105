import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Mail:
    """
    ShareNews class by default need the next instances:
        -mail = senders_mail
        -mail_to = who will receive the mail
        -password = mails password
        -smtp_server = The server of you mail provider
        -port = Default 465

    Mail Instances:
        self.message = MIMEMultipart("alternative")
        self.message["Subject"] = "News"
        self.message["From"] = self.mail
        self.message["To"] = self.destination
    """

    def __init__(self, mail, destination, password,
                 smtp_server, port='465', subject='News'):
        # Connection Instances
        self.mail = mail
        self.destination = destination
        self.password = password
        self.smtp_server = smtp_server
        self.port = port

        # two parts of message-> plain text and html content
        # change to message content
        self.subject = subject
        self.html = ''
        self.text = ''


    def create_message(self):
        # create message from mimemultipart obj
        # Mail / Message Instances
        self.content = MIMEMultipart("alternative")
        self.content["Subject"] = self.subject
        self.content["From"] = self.mail
        self.content["To"] = self.destination
        # create message
        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(self.text, "plain")
        part2 = MIMEText(self.html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        self.content.attach(part1)
        self.content.attach(part2)


    def send(self):
        # creating message
        self.create_message()
        # connecting to the mail client to send an email
        with smtplib.SMTP_SSL(self.smtp_server, self.port) as server:
            # login
            server.login(self.mail, self.password)
            # send
            server.sendmail(self.mail, self.destination, self.content.as_string())


    def send_to_many():
        pass
    