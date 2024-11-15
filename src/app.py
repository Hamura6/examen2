from flask import Flask, request, jsonify
from .config import Config, db_connection
app=Flask(__name__)
app.config.from_object(Config)
@app.route('/vehiculo',methods=['GET'])
def listar():
    con=db_connection(app)
    cursor=con.cursor()
    cursor.execute('SELECT * FROM vehiculo')
    vehiculos=cursor.fetchall()
    return jsonify(vehiculos),200
@app.route('/vehiculo/<int:id>',methods=['GET'])
def buscar(id):
    con=db_connection(app)
    cursor=con.cursor()
    cursor.execute('SELECT * FROM vehiculo WHERE placa=%s',(id))
    vehiculo=cursor.fetchone()
    column_names = [desc[0] for desc in cursor.description]
    vehiculo_dict = dict(zip(column_names, vehiculo))
    return jsonify(vehiculo_dict),200
@app.route('/vehiculo',methods=['POST'])
def create():
    con=db_connection(app)
    cursor=con.cursor()
    placa=request.json.get('placa')
    color=request.json.get('color')
    modelo=request.json.get('modelo')
    marca=request.json.get('marca')

    cursor.execute('INSERT INTO vehiculo (placa,color,modelo,marca) VALUES(%s,%s,%s,%s)',(placa,color,modelo,marca))
    con.commit()
    return jsonify('Vehiculo registrado'),220
@app.route('/vehiculo/<int:id>',methods=['PUT'])
def actualizar(id):
    con=db_connection(app)
    cursor=con.cursor()
    color=request.json.get('color')
    modelo=request.json.get('modelo')
    marca=request.json.get('marca')
    cursor.execute('UPDATE vehiculo SET color=%s,modelo=%s, marca=%s WHERE placa=%s',(color,modelo,marca,id))
    con.commit()
    return jsonify('El vehiculo fue actualizado'),220
@app.route('/vehiculo/<int:id>',methods=['DELETE'])
def delete(id):
    con=db_connection(app)
    cursor=con.cursor()
    cursor.execute('DELETE FROM vehiculo WHERE placa=%s',(id))
    con.commit()
    return jsonify('El vehiculo fue eliminada'),220
app.run(debug=True)
