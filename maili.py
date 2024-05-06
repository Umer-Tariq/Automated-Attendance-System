import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def send_copy(file_name):
    my_email = 'sendsystem8@gmail.com'
    password_key = 'ydgw mibv qeon pzcn'  # Update with your actual password
    nu_server = "smtp.gmail.com"
    nu_port = 587
    
    # Create a MIME multipart message
    msg = MIMEMultipart()
    msg['Subject'] = 'Sending Excel File'
    msg['From'] = my_email
    msg['To'] = 'saroshirfan786@gmail.com'  # Update with the recipient's email
    
    with open(excel_file_path, 'rb') as file:
        excel_attachment = MIMEApplication(file.read())
    
    excel_attachment.add_header('Content-Disposition', 'attachment', filename=file_name)
    msg.attach(excel_attachment)
    
    # Establish connection with the SMTP server
    with smtplib.SMTP(nu_server, nu_port) as my_server:
        my_server.ehlo()
        my_server.starttls()
        my_server.login(my_email, password_key)
        my_server.send_message(msg)

    print('Attendance sent successfully!')
