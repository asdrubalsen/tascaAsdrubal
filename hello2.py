from flask import Flask, render_template, request, redirect, url_for, make_response
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

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # Obtener los datos del formulario de inicio de sesión
        user = request.form['username']
        password = request.form['password']

        # Verificar si el usuario y la contraseña son correctos consultando la base de datos
        cursor.execute("SELECT Nombre FROM alumnos WHERE Nombre = %s AND Contraseña = %s", (user, password))
        resultado = cursor.fetchone()

        if resultado:
            # Si el usuario y la contraseña son correctos, establecer una cookie de sesión
            respuesta = make_response(redirect(url_for('dashboard', name=user)))
            respuesta.set_cookie('username', user)
            return respuesta
        else:
            # Si el usuario y la contraseña no son correctos, redirigir de nuevo a la página de inicio de sesión con un mensaje de error
            return render_template('home.html', error="Usuario o contraseña incorrectos")
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    # Eliminar la cookie de sesión y redirigir a la página de inicio
    respuesta = make_response(redirect(url_for('home')))
    respuesta.set_cookie('username', '', expires=0)
    return respuesta

@app.route('/dashboard/<name>')
def dashboard(name):
    # Verificar si el usuario está autenticado utilizando la cookie de sesión
    username = request.cookies.get('username')
    if username == name:
        # Usuario autenticado, mostrar el dashboard
        return render_template('logeado.html', name=name)
    else:
        # Usuario no autenticado, redirigir a la página de inicio
        return redirect(url_for('home'))

@app.route('/getmail', methods=['POST', 'GET'])
def getmail():
    if request.method == 'POST':
        user = request.form['name']
        return redirect(url_for('dashboard', name=user))
    else:
        user = request.args.get('name')
        return render_template('getmail.html')

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
