from flask import render_template, request, session, url_for
from . import estatTelefons



@estatTelefons.route('/', methods=['GET'])
def festatTelefons():
    # ... tu código actual (sin cambios)
    if "username" in session:
        return render_template('estat.html', titol="Estat telèfons")
    else:
        return "Accés prohibit."


