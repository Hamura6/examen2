from flask import Flask, request, jsonify
from config import Config, db_connection

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/vehiculo', methods=['GET'])
def listar():
    con = db_connection(app)
    cursor = con.cursor()
    cursor.execute('SELECT * FROM vehiculo')
    vehiculos = cursor.fetchall()
    return jsonify(vehiculos), 200

@app.route('/vehiculo/<string:placa>', methods=['GET'])
def buscar(placa):
    con = db_connection(app)
    cursor = con.cursor()
    cursor.execute('SELECT * FROM vehiculo WHERE placa=%s', (placa,))
    vehiculo = cursor.fetchone()
    
    if vehiculo:
        column_names = [desc[0] for desc in cursor.description]
        vehiculo_dict = dict(zip(column_names, vehiculo))
        return jsonify(vehiculo_dict), 200
    else:
        return jsonify({"error": "Vehículo no encontrado"}), 404

@app.route('/vehiculo', methods=['POST'])
def create():
    con = db_connection(app)
    cursor = con.cursor()
    placa = request.json.get('placa')
    color = request.json.get('color')
    modelo = request.json.get('modelo')
    marca = request.json.get('marca')

    cursor.execute('INSERT INTO vehiculo (placa, color, modelo, marca) VALUES (%s, %s, %s, %s)',
                   (placa, color, modelo, marca))
    con.commit()
    return jsonify({'message': 'Vehículo registrado'}), 201

@app.route('/vehiculo/<string:placa>', methods=['PUT'])
def actualizar(placa):
    con = db_connection(app)
    cursor = con.cursor()
    color = request.json.get('color')
    modelo = request.json.get('modelo')
    marca = request.json.get('marca')
    
    cursor.execute('UPDATE vehiculo SET color=%s, modelo=%s, marca=%s WHERE placa=%s',
                   (color, modelo, marca, placa))
    con.commit()

    if cursor.rowcount > 0:
        return jsonify({'message': 'Vehículo actualizado'}), 200
    else:
        return jsonify({'error': 'Vehículo no encontrado'}), 404

@app.route('/vehiculo/<string:placa>', methods=['DELETE'])
def delete(placa):
    con = db_connection(app)
    cursor = con.cursor()
    cursor.execute('DELETE FROM vehiculo WHERE placa=%s', (placa,))
    con.commit()

    if cursor.rowcount > 0:
        return jsonify({'message': 'Vehículo eliminado'}), 200
    else:
        return jsonify({'error': 'Vehículo no encontrado'}), 404

if __name__ == "__main__":
    app.run(debug=True)
