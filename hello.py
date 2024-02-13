from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def hello():
    return "Sí."

@app.route("/numero/<int:num>")
def numero(num):
    if num % 2 == 0:
        return "Par"
    else:
        return "Impar"

@app.route("/html/<nombre>/<int:edad>")
def hh(nombre=None, edad=None):
    year = 2023 + 100
    edad_futura = edad + 100
    return render_template('html5.html', age=edad_futura, name=nombre, year=year)












if __name__ == "__main__":
    app.run(debug=True)