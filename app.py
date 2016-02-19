from flask import Flask, redirect, url_for, request, render_template, request
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
        notas = Obtener_notas(usuario, request.form['password'])
        if notas:
            Ficha = getDict(notas)
        return render_template('pdf.html', data=dumps(Ficha, ensure_ascii=False), username=usuario)
    return redirect(url_for('404'))


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
