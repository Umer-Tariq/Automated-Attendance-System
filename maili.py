import smtplib 
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart 
import os

my_email='saroshirfan786@gmai.com'
password_key='F@st4878!'

# SMTP Server and port no for GMAIL.com
nu_server= "smtp.gmail.com"
nu_port= 587

# Starting connection
my_server = smtplib.SMTP(nu_server, nu_port)
my_server.ehlo()
my_server.starttls()
    
# Login with your email and password
my_server.login(my_email, password_key)


msg = MIMEMultipart() 
msg['Subject'] = '123hahaha' 
msg.attach(MIMEText('Hello from sarosh'))

my_server.sendmail(
            from_addr= my_email,
            to_addrs='umer.tariq3261@gmail.com',
            msg=msg
        )

my_server.quit()