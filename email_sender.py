import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders
from app_config import * 
import getpass

class EmailSender:
    
    @staticmethod 
    def send(filename:str):
        print(f"pls enter the password for {SENDER_EMAIL} in order to send the email")
        SENDER_PASSWORD =  getpass.getpass()
        msg = MIMEMultipart() 
        msg['From'] = SENDER_EMAIL
        msg['To'] = ", ".join(RECIPIENT_LIST)
        msg['Subject'] = "auto generated report"
        attachment = open(filename , "rb")
        p = MIMEBase('application', 'octet-stream') 
        p.set_payload((attachment).read()) 
        # encode into base64 
        encoders.encode_base64(p) 
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
        # attach the instance 'p' to instance 'msg' 
        msg.attach(p)
        # creates SMTP session 
        try:
            s = smtplib.SMTP('smtp.gmail.com', 587) 
            s.starttls() 
            s.login(SENDER_EMAIL, SENDER_PASSWORD) 
            text = msg.as_string() 
            s.sendmail(SENDER_EMAIL,RECIPIENT_LIST, text) 
            s.quit() 
        except  Exception as e:
            print(e)


