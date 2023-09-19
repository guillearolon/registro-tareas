from flask import Flask, render_template, request, url_for, redirect, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'clavesegura'

def crear_db():
    conexion = sqlite3.connect('registros.db')
    cursor = conexion.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS tareas(id INTEGER PRIMARY KEY AUTOINCREMENT,
                    incidente TEXT NOT NULL,
                   descripcion TEXT NOT NULL,
                   persona TEXT NOT NULL,
                   fecha DATE DEFAULT(DATE('now', 'localtime')))""")
    conexion.commit()
    conexion.close()


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':        
        if 'incidente' in request.form and 'descripcion' in request.form and 'persona' in request.form:
            with app.app_context():
                conexion = sqlite3.connect('registros.db')
                cursor = conexion.cursor()
                incidente = request.form.get('incidente')
                descripcion = request.form.get('descripcion')
                persona = request.form.get('persona')
                cursor.execute("INSERT INTO tareas (incidente, descripcion, persona) VALUES (?,?,?)", (incidente, descripcion, persona,))
                conexion.commit()
                conexion.close()
            flash('Datos cargados con exito', 'success')    
            return redirect(url_for('index'))
        
    with app.app_context():
        conexion = sqlite3.connect('registros.db')
        cursor = conexion.cursor()
        datos = cursor.execute("SELECT * FROM tareas").fetchall()
        conexion.commit()
        conexion.close()

    return render_template('index.html', datos=datos)
    

@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    with app.app_context():
        conexion = sqlite3.connect('registros.db')
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM tareas WHERE id = ?", (id,))
        conexion.commit()
        conexion.close()

    return redirect(url_for('index'))    



if __name__ == '__main__':
    crear_db() 
    app.run('localhost', debug=True)