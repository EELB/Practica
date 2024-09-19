from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

def get_db_connection():
    connection =  pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='101',
        cursorclass=pymysql.cursors.DictCursor)
    return connection

# Ruta para obtener los usuarios
@app.route('/api/usuarios', methods=['GET'])
def get_usuarios():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql ="SELECT id, nombre, email FROM usuarios"
        cursor.execute(sql)
        usuarios = cursor.fetchall()
    connection.close()
    return jsonify(usuarios)

# Ruta para insertar un usuario
@app.route('/api/usuarios', methods=['POST'])
def create_usuario():
    content = request.json  # Capturamos los datos del cuerpo de la solicitud
    nombre = content.get('nombre')
    email = content.get('email')

    # Validación básica para verificar que los campos no están vacíos
    if not nombre or not email:
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO usuarios (nombre, email) VALUES (%s, %s)"
            cursor.execute(sql, (nombre, email))
            connection.commit()  # Confirmamos la transacción
        return jsonify({"message": "Usuario creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

# Ruta de bienvenida
@app.route('/')
def home():
    return jsonify({
        "message" : "Bienvenido a la API Flask DSM 101"
    })

# Ruta de ejemplo GET
@app.route('/api/data', methods=['GET'])
def det_data_get():
    content_body = {
        "name": "Ricardo",
        "last_name": "Lugo"
    }
    return jsonify(content_body)

# Ruta de ejemplo POST
@app.route('/api/data', methods=['POST'])
def det_data_post():
    content_body = request.json
    print("******************")
    print(content_body)
    print("******************")
    return jsonify({
        "received" : content_body
    })

if __name__ == '__main__':
    app.run(debug=False)
