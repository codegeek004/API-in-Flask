from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for, session
import requests
import json
import time
app = Flask(__name__)
app.secret_key = 'yash123'

myapp = Blueprint('myapp', __name__)
app.register_blueprint(myapp)

@app.route('/', methods=['GET'])
def api_view():
	response = requests.get('http://127.0.0.1:8000')
	print('response', response)
	print(response.content)
	content = response.content
	content = json.loads(content)
	print(content, 'json content')
	for i, j in content.items():
		data = j
	return render_template('index.html', data=data)

@app.route('/login', methods=['GET',	"POST"])
def login_view():
	login_url = 'http://127.0.0.1:8000/accounts/login/'

	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		creds = {'username': username, 'password':password}
		try:
			login = requests.post(login_url, data=creds)

			if login.status_code == 200:
				data = login.json()
				print('data', data)
				token = data.get('access')
				print('token', token)
				session['token'] = token
				return "user login successful"
			else:
				return "Invalid credentials"
		except Exception as e:
			print('e',e)

	return render_template('login.html')

@app.route('/vehicles', methods=['GET','POST'])
def vehicle_view():
	vehicle_url = 'http://127.0.0.1:8000/vehicles/'
	token = session.get('token')
	if not token:
		print(session)
		return redirect(url_for('login_view'))
	headers = {'Authorization':f'Bearer {token}'}

	try:
		response = requests.get(vehicle_url, headers=headers)
		print('response', response)
		if response.status_code == 200:
			print('inside if 200')
			data = response.json()
			print('response.json', data)
			return render_template('vehicle.html', data=data)
		else:
			return "Creds not provided"
	except Exception as e:
		# return 'exception mai gaya'
		print('e',e)
		time.sleep(5)
	return render_template('vehicle.html')


@app.route('/slots/', methods=['GET','POST'])
def slot_view():
	vehicle_url = 'http://127.0.0.1:8000/slots/'
	token = session.get('token')
	if not token:
		print(session)
		return redirect(url_for('login_view'))
	headers = {'Authorization':f'Bearer {token}'}

	try:
		response = requests.get(vehicle_url, headers=headers)
		print('response', response)
		if response.status_code == 200:
			data = response.json()
			data = json.loads(data)
			return render_template('vehicle.html', data=data)
		else:
			return "Creds not provided"
	except Exception as e:
		# return 'exception mai gaya'
		print('e',e)
		time.sleep(5)
	return render_template('vehicle.html')


if __name__=='__main__':
	app.run(debug=True, port=5000)