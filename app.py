from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from mail import email

app = Flask(__name__)

ENV = 'dev'
if ENV == 'dev':
	app.debug = True
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/apple'
else:
	app.debug = False
	app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
	__tablename__ = 'feedback'
	id = db.Column(db.Integer, primary_key = True)
	customer = db.Column(db.String(200), unique = True)
	product = db.Column(db.String(200))
	rating = db.Column(db.Integer)
	comments = db.Column(db.Text())

	def __init__(self, customer, product, rating, comments):
		self.customer = customer
		self.product = product
		self.rating = rating
		self.comments = comments
		

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
	if request.method == 'POST':
		customer = request.form['customer']
		product = request.form['product']
		rating = request.form['rating']
		comments = request.form['comments']
		if customer == '' or product == '':
			return render_template('index.html', message = 'Please fill in your name & product type')
		if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
			data = Feedback(customer, product, rating, comments)
			db.session.add(data)
			db.session.commit()
			email(customer, product, rating, comments)
			return render_template('success.html')
		return render_template('index.html', message = 'Feedback already submitted for the user.')

if __name__ == '__main__':
	app.run()