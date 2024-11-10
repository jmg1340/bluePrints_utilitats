from flask import render_template, request, session, url_for
from . import login


@login.route('/', methods=['GET', 'POST'])
def fLogin():
	if request.method == 'POST':
			print( "estic a POST")
			dataFromLoginForm = request.get_json() 
			print("dataFromLoginForm", dataFromLoginForm)
			print("dataFromLoginForm['pwd']", dataFromLoginForm['pwd'])

			if dataFromLoginForm['pwd'] == "jordi":
				session['username'] = 'usuariAnonim'
				return {'pwdValid': True }
			else:
				return {'pwdValid': False, "missatge": "PASSWORD INCORRECTE" } 

	return render_template( 'login.html' )
