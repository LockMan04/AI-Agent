import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

try: 
    sender_email = os.getenv("SMTP_USERNAME")  
    sender_password = os.getenv("SMTP_PASSWORD")
    
    if not sender_email or not sender_password:
        raise ValueError("SMTP_USERNAME and SMTP_PASSWORD must be set in the environment variables.")
    
except Exception as e:
    print(f"Error loading environment variables: {e}")


def send_mail(receiver_email, subject, body):

  msg = MIMEMultipart()
  msg['From'] = sender_email
  msg['To'] = receiver_email
  msg['Subject'] = subject

  msg.attach(MIMEText(body, 'html'))

  try:
      server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
      server.ehlo()
      server.login(sender_email, sender_password)
      server.sendmail(sender_email, receiver_email, msg.as_string())
      server.close()

      print('Đã gửi thư thành công')
      return True
  except Exception as e:
      print(f"Lỗi khi gửi email: {e}")
      return False