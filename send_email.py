import smtplib
from email.message import EmailMessage
import os

USER_EMAIL = os.environ.get("EMAIL_USER")
USER_PASSWORD = os.environ.get("EMAIL_PASS")

files = ["amazon_products.xlsx", "flipkart.xlsx"]

def send_email(to_email):
	msg = EmailMessage()
	msg['Subject'] = "Price of products from various e-comm websites."
	msg['From'] = 'USER_EMAIL'
	msg['To'] = to_email
	msg.set_content('Product prices scraped from multiple e-comm site.')
	for file in files:
		with open(file, 'rb') as f:
			file_data = f.read()
			msg.add_attachment(file_data, maintype = "apllication", 
								subtype = "xlsx", filename = f.name)
	
	with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
		smtp.login(USER_EMAIL, USER_PASSWORD)
		smtp.send_message(msg)
		
 
