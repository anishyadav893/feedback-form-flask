import smtplib
from email.mime.text import MIMEText

def email(customer, product, rating, comments):
	port = 2525
	server = 'smtp.mailtrap.io'
	login = '4cc8b503b8ea0a'
	password = 'ddb6272928de1d'

	message = f'<h3>Feedback Submission</h3><ul><li>Customer: {customer}</li><li>Product: {product}</li><li>Rating: {rating}</li><li>Comments: {comments}</li></ul>'

	sender = 'sample@example.com'
	receiver = 'sample2@example.com'
	msg = MIMEText(message, 'html')
	msg['Subject'] = 'Apple Feedback Form'
	msg['From'] = sender
	msg['To'] = receiver

	with smtplib.SMTP(server, port) as my_server:
		my_server.login(login, password)
		my_server.sendmail(sender, receiver, msg.as_string())