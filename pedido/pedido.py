from flask import Blueprint, render_template, request, session
import flask
import psycopg2
import psycopg2.extras

from functions.functions import tuple_to_dict


POSTGRESQL_URI = "postgres://nrzaptwjbceonc:85e6f9cb1eb0447157fa9de8cc08cd804f02a1e555b5747860ec3a6d9f9140a0@ec2-35-153-91-18.compute-1.amazonaws.com:5432/d939kg82f0uljg"
pedidoBP = Blueprint('pedido', __name__, template_folder='templates', static_folder='static')
connection = psycopg2.connect(POSTGRESQL_URI)


@pedidoBP.route('/pedido/pedido-finalizado/<id>')
def pedido_finalizado(id):
    authenticate =  session if 'google_id' in session else False
    with connection.cursor() as cursor: 
        cliente = False
        user = False
        if authenticate:
            sql = """SELECT * FROM madarah.tb_usuario WHERE google_id = '""" + authenticate['google_id'] + """' LIMIT 1"""
            cursor.execute(sql)
            user = tuple_to_dict(cursor.description, cursor.fetchone())

            sql = """SELECT * FROM madarah.tb_cliente WHERE id_usuario = """ + str(user['id_usuario']) + """ LIMIT 1"""
            cursor.execute(sql)
            cliente = tuple_to_dict(cursor.description, cursor.fetchone())

            sql = """SELECT * 

                    FROM madarah.tb_pedido as p
                    WHERE id = %s LIMIT 1"""
            cursor.execute(sql)
            pedido = tuple_to_dict(cursor.description, cursor.fetchone())

        session['usuario'] = user
        session['cliente'] = cliente

    return render_template('pedido-finalizado.html', auth=authenticate, cliente=cliente, usuario=user)


@pedidoBP.route('/cadastro_pedido', methods=['GET', 'POST'])
def cadastro_pedido():
    if flask.request.method == 'POST':
        connection = psycopg2.connect(POSTGRESQL_URI)
        id_cliente_usuario = int(request.form['id_cliente_usuario']),
        nome = str(request.form['nome']),
        endereco = str(request.form['endereco']),
        telefone1 = str(request.form['cep']),
        telefone2 = float(request.form['telefone'])
        with connection.cursor() as cursor:
            sql = """insert into madarah.tb_pedido (id_cliente_usuario, nome, endereco, telefone1, telefone2) VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(sql, (id_cliente_usuario, nome, endereco, telefone1, telefone2))
            cursor.close()
            connection.commit()
    
    return render_template('cadastro_pedido.html')



@pedidoBP.route('/editar_pedido', methods=['POST', 'GET'])
def edicao_pedido():
    if flask.request.method == 'POST':
        id_cliente_usuario = int(request.form['id_cliente_usuario']),
        nome = str(request.form['nome']),
        endereco = str(request.form['endereco']),
        telefone1 = str(request.form['cep']),
        telefone2 = float(request.form['telefone'])
        connection = psycopg2.connect(POSTGRESQL_URI)
        with connection.cursor() as cursor:
            sql = """update madarah.tb_pedido SET nome = (%s), endereco = (%s), telefone1 = (%s), telefone2 = (%s) WHERE id_cliente_usuario = (%s)"""
            cursor.execute(sql, ( nome, endereco, telefone1, telefone2, id_cliente_usuario))
            cursor.close()
            connection.commit()
    return render_template('edit_pedido.html')



@pedidoBP.route('/pedidos', methods=['GET'])
def list_pedidos():
    connection = psycopg2.connect(POSTGRESQL_URI)    
    with connection.cursor() as cursor:
        sql = """select * from madarah.tb_pedido order by id"""
        cursor.execute(sql)
        lista = cursor.fetchall()
    return render_template("list_pedidos.html", pedidos=lista)



@pedidoBP.route('/delete_pedido/<int:id>', methods=['POST', 'GET'])
def delete_pedido(id):
    connection = psycopg2.connect(POSTGRESQL_URI)    
    with connection.cursor() as cursor:
        sql = """delete madarah.tb_pedido where id = (%s)"""
        cursor.execute(sql, id)
        lista = cursor.fetchall()
    return render_template('delete_pedido.html')
