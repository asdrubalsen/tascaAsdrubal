from flask import Flask, render_template, request, redirect, url_for, session, send_file
import mysql.connector

app = Flask(__name__)
app.secret_key = 'hola joan'

# Configuración de la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="Asdrúbal",
    password="Admin22.",
    database="listacorreo"
)
cursor = db.cursor()

# Rutas de la aplicación
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['correo']
        password = request.form['password']
        cursor.execute("SELECT * FROM alumnos WHERE correo = %s AND contraseña = %s", (email, password))
        user = cursor.fetchone()
        if user:
            session['username'] = user[1]
            return redirect(url_for('privado'))
        else:
            return render_template('login.html', message='Usuario o contraseña incorrectos')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor.execute("INSERT INTO alumnos (nombre, correo, contraseña) VALUES (%s, %s, %s)", (username, email, password))
        db.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

@app.route('/public-section')
def public():
    return render_template('publico.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        email = request.form['email']
        contraseña = request.form['contraseña']
        username = request.form['nombre']
        
        # Verificar si el correo electrónico ya está en la base de datos
        cursor.execute("SELECT correo FROM alumnos WHERE correo = %s", (email,))
        correo_existente = cursor.fetchone()
        
        if correo_existente:
            # Si el correo ya existe, mostrar un mensaje de error
            return ("El correo electrónico ya está registrado.")
        else:
            # Si el correo no existe, insertar el nuevo usuario en la base de datos
            cursor.execute("INSERT INTO alumnos (nombre, correo, contraseña) VALUES (%s, %s, %s)", (username, email, contraseña))
            db.commit()
            return render_template('registrado.html')
    
    return render_template('registro.html')


# Ruta para la página de registro exitoso
@app.route('/registro_exitoso')
def registro_exitoso():
    return '¡Registro exitoso!'

@app.route('/privado')
def privado():
    return render_template('privado.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contacto', methods=['POST'])
def contacto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        mensaje = request.form['mensaje']
        
        # Insertar el mensaje en la base de datos
        cursor.execute("INSERT INTO sugerencias (nombre, email, comentario) VALUES (%s, %s, %s)", (nombre, email, mensaje))
        db.commit()
        
        return render_template('publico.html')

@app.route('/descargar', methods=['GET'])
def descargar_archivo():
    # Ruta al archivo que deseas descargar
    ruta_archivo = 'static/imagenes/3632102.jpg'
    # Nombre del archivo que se descargará
    nombre_archivo = 'imagen.jpg'
    # Utiliza send_file para enviar el archivo al cliente
    return send_file(ruta_archivo, as_attachment=True, download_name=nombre_archivo)

if __name__ == '__main__':
    app.run(debug=True)