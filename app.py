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

slot_url = 'http://127.0.0.1:8000/slots/'
@app.route('/slots/', methods=['GET'])
def slot_view():
    token = session.get('token')
    if not token:
        print(session)
        return redirect(url_for('login_view'))
    headers = {'Authorization':f'Bearer {token}'}
    try:
        response = requests.get(slot_url, headers=headers)
        print(response)
        if response.status_code == 200:
            slots = response.json()
            return render_template('slots.html', data=slots)
        else:
            return "Failed to fetch data"
    except Exception as e:
        print('e',e)
        # return jsonify({"error": str(e)})

@app.route('/slots/add', methods=['GET', 'POST'])
def create_slot():
    if request.method == 'POST':
        space = request.form.get('space')
        price = request.form.get('price')
        total_slots = request.form.get('total_slots')
        
        data = {
            "space": space,
            "price": price,
            "total_slots": total_slots
        }

        token = session.get('token')
        if not token:
            print(session)
            return redirect(url_for('login_view'))

        headers = {'Authorization': f'Bearer {token}'}
        
        try:
            response = requests.post(slot_url, json=data, headers=headers)
            if response.status_code == 201:
                flash("New slot added successfully", "success")
            else:
                flash("Failed to add new slot", "error")
        except Exception as e:
            print('Error:', e)
            flash("An error occurred while adding the slot", "error")
        
        return redirect(url_for('slot_view'))
    
    return render_template('add_slot.html')


@app.route('/slots/<int:slot_id>/update', methods=['GET'])
def update_slot_form(slot_id):
    token = session.get('token')
    if not token:
        print(session)
        return redirect(url_for('login_view'))
    headers = {'Authorization':f'Bearer {token}'}
    try:
        response = requests.get(f"{slot_url}{slot_id}/", headers=headers)
        if response.status_code == 200:
            slot = response.json()
            return render_template('update_slot.html', slot=slot)
        else:
            flash("Slot not found", "error")
            return redirect(url_for('slot_view'))
    except Exception as e:
        print('e',e)
        return redirect(url_for('slot_view'))


@app.route('/slots/<int:slot_id>/update', methods=['POST'])
def update_slot(slot_id):

    space = request.form['space']
    price = request.form['price']
    total_slots = request.form['total_slots']
    
    data = {
        "space": space,
        "price": price,
        "total_slots": total_slots
    }
    token = session.get('token')
    if not token:
        print(session)
        return redirect(url_for('login_view'))
    headers = {'Authorization':f'Bearer {token}'}
    try:
        response = requests.put(f"{slot_url}{slot_id}/", json=data, headers=headers)
        if response.status_code == 200:
            flash("Slot updated successfully", "success")
        else:
            flash("Failed to update slot", "error")
    except Exception as e:
        print('e',e)
    
    return redirect(url_for('slot_view'))


@app.route('/slots/<int:slot_id>/delete', methods=['POST'])
def delete_slot(slot_id):
    token = session.get('token')
    if not token:
        return redirect(url_for('login_view'))

    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        response = requests.delete(f"{slot_url}{slot_id}/", headers=headers)
        if response.status_code == 204:
            flash(f"Slot {slot_id} deleted successfully", "success")
        else:
            flash("Failed to delete slot", "error")
    except Exception as e:
        print('Error:', e)
        flash("Error occurred while deleting slot", "error")


    return redirect(url_for('slot_view'))





if __name__=='__main__':
	app.run(debug=True, port=5000)