from flask import Flask, session, redirect, url_for, request, render_template, request
from generateJson import getDict
from pucAssist import Obtener_notas
from json import dumps

app = Flask(__name__)
app.secret_key = b'\xb0\x10l\xf4f?n\n\xc5\x9bbZd\xfd\x06\xa2\xa8\xf8\xdcy\x1f\xe1\xf4\xa7'


@app.route("/")
def index():
    """ Pagina principal """
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    """ Destino del POST hecho con las credenciales """
    if request.method == 'POST':
        usuario = request.form['usuario']
        session[usuario] = request.form['password']
        return redirect(url_for('inside', user=usuario))
    return redirect(url_for('404'))  # Metodo no permitido


@app.route("/inside/<user>")
def inside(user):
    """ Verificacion de credenciales """
    Notas = Obtener_notas(user, session[user])
    session.pop(user, None)
    if Notas:
        Ficha = getDict(Notas)
        return render_template('pdf.html', data=dumps(Ficha, ensure_ascii=False), username=user)
    return redirect(url_for('404'))  # Logeo incorrecto


@app.route("/out", methods=['POST'])
def out():
    """ Pagina de salida """
    return render_template('out.html')

if __name__ == "__main__":
    import os
    app.run(
        host='0.0.0.0',
        debug=True,
        port=int(os.environ.get("PORT", 5000))
    )
