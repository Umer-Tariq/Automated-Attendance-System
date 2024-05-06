from pickle import TRUE
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string
import time

def generate_string(length):
  list = string.ascii_lowercase + string.ascii_uppercase + string.punctuation + string.digits
  verif_code = ''
  for i in range(0, length):
    verif_code += str(random.choice(list))

  return verif_code

def otp_msg():
  my_email = 'sendsystem8@gmail.com'
  password_key = 'ydgw mibv qeon pzcn'
  nu_server = "smtp.gmail.com"
  nu_port = 587
  id = input(print('Enter your id for otp : '))
  parts = id.split('-')
  recipient_email = parts[0] + parts[1] +'@nu.edu.pk'
  print(recipient_email)
  code = generate_string(8)
  # HTML content with a bold heading and bigger font size
  html_content = f"""
  <html>
    <head></head>
    <body>
      <p style="font-size: 16px;">Hey {id}!</p>
      <h1 style="font-size: 24px; font-weight: bold;">Your Verificaion Code is {code} </h1>
      <p style="font-size: 16px;">Enter this verification code, to mark your attendance.</p>
      <p style="font-size: 16px;">In case of any query, please contact your student affairs.</p>
      <br>
      <p style="font-size: 16px;">Regards,</p>
      <p style="font-size: 16px;">team</p>
    </body>
  </html>
  """

  msg = MIMEMultipart()
  msg['Subject'] = 'Verification Code'
  msg['From'] = my_email
  msg['To'] = recipient_email  # Update with the recipient's email

  # Create a MIMEText object with the HTML content and attach it to the message
  body = MIMEText(html_content, 'html')
  msg.attach(body)

  with smtplib.SMTP(nu_server, nu_port) as my_server:
      my_server.ehlo()
      my_server.starttls()
      my_server.login(my_email, password_key)
      my_server.send_message(msg)

  print('Email sent successfully!')

  print(code)
  entered_code = ''
  start_time = time.time()
  while time.time() - start_time < 20 and len(entered_code ) <= 0:
    entered_code = input(print("Enter Verification Code here : "))
    if entered_code == code and time.time() - start_time < 20:
      print('verifing...')
      return True

  print('code expired')
  return False

