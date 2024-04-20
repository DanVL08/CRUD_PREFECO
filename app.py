from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from MySQLdb import ProgrammingError
app = Flask(__name__)

#MYSQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'prefeco_db'
mysql = MySQL(app)

#settings
app.secret_key = 'mysecretkey'

#RUTA INICIO, aparecerá la pantalla para mostrar o registrar alumnos
@app.route('/')
def index():
    #SE OBTIENEN LOS DATOS DE LA BD Y SE RETORNAN PLASMADOS EN index.html
    try:
        cursor = mysql.connection.cursor()
        sql = 'SELECT * from alumnos'
        cursor.execute(sql)
        datos = cursor.fetchall()
        return render_template('index.html', alumnos = datos)
    except Exception as e:
        flash(e)
        return redirect(url_for('index'))
#RUTA INICIO, aparecerá la pantalla para mostrar o registrar pagos
@app.route('/pagos')
def index_pagos():
    #SE OBTIENEN LOS DATOS DE LA BD Y SE RETORNAN PLASMADOS EN pagos.html
    try:
        cursor = mysql.connection.cursor()
        sql = 'SELECT * from pagos'
        cursor.execute(sql)
        datos = cursor.fetchall()
        return render_template('pagos.html', pagos = datos)
    except Exception as e:
        flash(e)
        return redirect(url_for('index'))
#RUTA PARA AÑADIR ALUMNOS NUEVOS
@app.route('/add_contact', methods=['POST'])
def add_contact():
    #SOLICITAR LOS DATOS DEL FORMULARIO DE index.html
    if request.method == 'POST':
        try:
            nombres = request.form['nombres']
            apellido1 = request.form['apellido1']
            apellido2 = request.form['apellido2']
            fecha_nacimiento = request.form['fecha_nacimiento']
            grado = request.form['grado']
            grupo = request.form['grupo']
            matricula = request.form['matricula']
            direccion = request.form['direccion']
            telefono = request.form['telefono']

        #SUBIR LOS DATOS DEL FORMULARIO A LA BASE DE DATOS
            cursor = mysql.connection.cursor()
            sql = """
        INSERT INTO alumnos (nombre, apellido1, apellido2, fecha_nacimiento, grado, grupo, matricula, direccion, telefono)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            valores = (nombres, apellido1, apellido2, fecha_nacimiento, grado, grupo, matricula, direccion, telefono)

            cursor.execute(sql, valores)
            mysql.connection.commit()

            flash('Contacto agregado satisfactoriamente')
            return redirect(url_for('index'))
        except Exception as e:
            flash(e)
            return redirect(url_for('index'))
#RUTA PARA AÑADIR PAGOS NUEVOS
@app.route('/agregar_pago', methods=['POST'])
def agregar_pago():
    #SOLICITAR LOS DATOS DEL FORMULARIO DE pagos.html
    if request.method == 'POST':
        try:
            cursor = mysql.connection.cursor()

            matricula = request.form['matricula']

            # Obtener datos no visibles a partir de la matricula
            cursor.execute("SELECT alumno_id FROM alumnos WHERE matricula = %s", (matricula,))
            alumno_id = cursor.fetchone()

            if not alumno_id:
                flash('No se encontró ningún alumno con la matrícula proporcionada')
                return redirect(url_for('index_pagos'))

            fecha_pago = request.form['fecha_pago']
            monto = request.form['monto']
            metodo_pago = request.form['metodo_pago']
            estado_pago = request.form['estado_pago']
            concepto_pago = request.form['concepto_pago']

            #SUBIR LOS DATOS DEL FORMULARIO A LA BASE DE DATOS
            sql = """
            INSERT INTO pagos (alumno_id, matricula, fecha_pago, monto, metodo_pago, estado_pago, concepto_pago)
            VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            valores = (alumno_id[0], matricula, fecha_pago, monto, metodo_pago, estado_pago, concepto_pago)

            cursor.execute(sql, valores)
            mysql.connection.commit()

            flash('Pago agregado satisfactoriamente')
            return redirect(url_for('index_pagos'))
        
        except ProgrammingError as ex:
            flash('Error de base de datos: ' + str(ex))
            return redirect(url_for('index_pagos'))
        
        except Exception as ex:
            flash('Error inesperado: ' + str(ex))
            return redirect(url_for('index_pagos'))

#EJECUTA LA CONSULTA SQL PARA OBTENER UN ALUMNO PARA EDITAR
@app.route('/edit/<id>')
def get_contact(id):
        try:
            cursor =  mysql.connection.cursor()
            cursor.execute('SELECT * FROM  alumnos WHERE alumno_id = %s', (id,))
            datos = cursor.fetchall()
            print(datos[0])
            #ENVIA LOS DATOS A editar-alumno.html y los muestra en la hoja
            return render_template('editar-alumno.html',alumno = datos[0])
        except Exception as e:
            flash(e)
            return redirect(url_for('index'))
#SE ENCARGA DE ENVIAR LOS DATOS ACTUALIZADOS DEL FORMULARIO A LA BD
@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    #SOLICITAR LOS DATOS DEL FORMULARIO DE editar-alumno.html
    if request.method == 'POST':
        try:
            nombres = request.form['nombres']
            apellido1 = request.form['apellido1']
            apellido2 = request.form['apellido2']
            fecha_nacimiento = request.form['fecha_nacimiento']
            grado = request.form['grado']
            grupo = request.form['grupo']
            matricula = request.form['matricula']
            direccion = request.form['direccion']
            telefono = request.form['telefono']
            cursor = mysql.connection.cursor()
            #SUBIR LOS DATOS DEL FORMULARIO A LA BASE DE DATOS
            cursor.execute("""
                UPDATE alumnos
                SET nombre = %s, apellido1 = %s, apellido2 = %s,
                    fecha_nacimiento = %s, grado = %s, grupo = %s,
                    matricula = %s, direccion = %s, telefono = %s
                WHERE alumno_id = %s
            """, (nombres, apellido1, apellido2, fecha_nacimiento, grado, grupo, matricula, direccion, telefono, id))
            mysql.connection.commit()
            flash('Alumno actualizado satisfactoriamente.')
            return(redirect(url_for('index')))
        except Exception as e:
            flash(e)
            return redirect(url_for('index'))
#EJECUTA LA CONSULTA SQL PARA OBTENER UN PAGO PARA EDITAR
@app.route('/editar-pago/<id>')
def get_pago(id):
    try:
        cursor =  mysql.connection.cursor()
        cursor.execute('SELECT * FROM  pagos WHERE pago_id = %s', (id,))
        datos = cursor.fetchall()
        print(datos[0])
        #ENVIA LOS DATOS A editar-pago.html y los muestra en la hoja
        return render_template('editar-pago.html',pago = datos[0])
    except Exception as e:
        flash(e)
        return redirect(url_for('index_pagos'))
#SE ENCARGA DE ENVIAR LOS DATOS ACTUALIZADOS DEL FORMULARIO A LA BD
@app.route('/actualizar-pago/<id>', methods = ['POST'])
def update_pago(id):
    #SOLICITAR LOS DATOS DEL FORMULARIO DE editar-pago.html
    if request.method == 'POST':
        try:
            cursor = mysql.connection.cursor()

            matricula = request.form['matricula']

            # Obtener datos no visibles a partir de la matricula
            cursor.execute("SELECT alumno_id FROM alumnos WHERE matricula = %s", (matricula,))
            alumno_id = cursor.fetchone()

            if not alumno_id:
                flash('No se encontró ningún alumno con la matrícula proporcionada')
                return redirect(url_for('index_pagos'))
            # Obtener datos no visibles a partir de la matricula
            cursor.execute("SELECT alumno_id FROM alumnos WHERE matricula = %s", (matricula,))
            alumno_id = cursor.fetchone()

            if not alumno_id:
                flash('No se encontró ningún pago relacionado con la matrícula proporcionada')
                return redirect(url_for('index_pagos'))
            fecha_pago = request.form['fecha_pago']
            monto = request.form['monto']
            metodo_pago = request.form['metodo_pago']
            estado_pago = request.form['estado_pago']
            concepto_pago = request.form['concepto_pago']
            #SUBIR LOS DATOS A LA BD
            cursor.execute("""
                UPDATE pagos
                SET matricula = %s, fecha_pago = %s, monto = %s,
                    metodo_pago = %s, estado_pago = %s, concepto_pago = %s
                WHERE pago_id = %s
            """, (matricula, fecha_pago, monto, metodo_pago, estado_pago, concepto_pago, id))
            mysql.connection.commit()
            flash('Pago actualizado satisfactoriamente.')
            return(redirect(url_for('index_pagos')))
        
        except ProgrammingError as ex:
            flash('Error de base de datos: ' + str(ex))
            return redirect(url_for('index_pagos'))
        
        except Exception as ex:
            flash('Error inesperado: ' + str(ex))
            return redirect(url_for('index_pagos'))

#ELIMINA UN ALUMNO A APARTIR DE SI ID
@app.route('/delete/<string:id>')
def delete_contact(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM alumnos WHERE  alumno_id = {0}'.format(id))
        mysql.connection.commit()
        flash('Alumno eliminado exitosamente')
        return redirect(url_for('index'))
    except Exception as e:
        flash(e)
        return redirect(url_for('index_pagos'))
#ELIMINA UN PAGO A APARTIR DE SI ID
@app.route('/borrar-pago/<id>')
def delete_pago(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM pagos WHERE  pago_id = {0}'.format(id))
        mysql.connection.commit()
        flash('Pago eliminado exitosamente')
        return redirect(url_for('index_pagos'))
    except Exception as e:
        flash(e)
        return redirect(url_for('index_pagos'))
if __name__ == '__main__':
    app.run(port = 3000, debug=True)