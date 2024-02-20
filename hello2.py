from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Establecer la conexión a la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="Asdrúbal",
    password="Admin22.",
    database="listacorreo"
)

# Crear el cursor
cursor = conexion.cursor()

@app.route('/')
def home():
    # Página inicial
    return render_template('home.html')

@app.route('/dashboard/<name>')
def dashboard(name):
    # Consultar el correo electrónico del usuario
    cursor.execute("SELECT Correo FROM alumnos WHERE Nombre = %s", (name,))
    resultado = cursor.fetchone()

    if resultado:
        correo = resultado[0]
        return '¡Bienvenido ' + name + '!, Tu correo electrónico es: %s' % correo
    else:
        return 'Usuario no encontrado'

@app.route('/getmail', methods=['POST', 'GET'])
def getmail():
    if request.method == 'POST':
        user = request.form['name']
        return redirect(url_for('dashboard', name=user))
    else:
        user = request.args.get('name')
        return render_template('login.html')

@app.route('/addmail', methods=['GET', 'POST'])
def addmail():
    if request.method == 'POST':
        user = request.form['name']
        Correo = request.form['email']

        # Insertar nuevo usuario en la base de datos
        cursor.execute("INSERT INTO alumnos (Nombre, Correo) VALUES (%s, %s)", (user, Correo))
        conexion.commit()

        return redirect(url_for('dashboard', name=user))
    else:
        return render_template('addmail.html')

if __name__ == '__main__':
    app.run(debug=True)

# Cerrar cursor y conexión al finalizar
cursor.close()
conexion.close()
