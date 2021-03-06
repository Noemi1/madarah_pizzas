from functions.functions import rows_to_dict, tuple_to_dict
from flask import Blueprint, render_template, request, session
import flask
import psycopg2
import psycopg2.extras

POSTGRESQL_URI = "postgres://nrzaptwjbceonc:85e6f9cb1eb0447157fa9de8cc08cd804f02a1e555b5747860ec3a6d9f9140a0@ec2-35-153-91-18.compute-1.amazonaws.com:5432/d939kg82f0uljg"
pizzaBP = Blueprint('pizza', __name__, template_folder='templates', static_folder='static')
connection = psycopg2.connect(POSTGRESQL_URI)

@pizzaBP.route('/cardapio', methods=['GET'])
def cardapio():
    with connection.cursor() as cursor:
        sql = """SELECT * FROM madarah.tb_pizza WHERE ativo = true order by sabor"""
        cursor.execute(sql)
        lista = rows_to_dict(cursor.description, cursor.fetchall())
        cliente = session['cliente'] or False
        usuario = session['usuario'] or False
        auth = session if usuario else False
    return render_template("cardapio.html", pizzas=lista, cliente=cliente, usuario=usuario, auth=auth)

@pizzaBP.route('/pizzas', methods=['GET'])
def list():
    connection = psycopg2.connect(POSTGRESQL_URI)
    with connection.cursor() as cursor:
        sql = """SELECT * FROM madarah.tb_pizza WHERE ativo = true order by sabor"""
        cursor.execute(sql)
        lista = rows_to_dict(cursor.description, cursor.fetchall())
        cliente = session['cliente']
        usuario = session['usuario']
    return render_template("list.html", pizzas=lista, cliente=cliente, usuario=usuario, auth=session)


@pizzaBP.route('/pizza/cadastro', methods=['GET'])
def cadastro_pizza_get():
    # return render_template('cadastrar_pizza.html', cliente=cliente, usuario=usuario, auth=session)
    return render_template('cadastrar_pizza.html')


@pizzaBP.route('/pizza/cadastro', methods=['POST'])
def cadastro_pizza_post():
    sabor = str(request.form['sabor']),
    descricao = str(request.form['descricao']),
    valor = request.form['valor'].replace('.', ',').replace(',', '.')
    valor = float(valor)
    url_foto = str(request.form['url_foto'])
    connection = psycopg2.connect(POSTGRESQL_URI)
    with connection.cursor() as cursor:
        sql = """insert into madarah.tb_pizza (sabor, descricao, valor, url_foto, ativo) VALUES (%s, %s, %s, %s, true)"""
        cursor.execute(sql, (sabor, descricao, valor, url_foto))
        connection.commit()
        cursor.close()
    return '/pizzas'



@pizzaBP.route('/pizza/edicao/<id>', methods=['GET'])
def edicao_pizza_get(id):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM madarah.tb_pizza WHERE id_pizza = " + id
        cursor.execute(sql)
        pizza = tuple_to_dict(cursor.description, cursor.fetchone())
    return render_template('editar_pizza.html', pizza=pizza)


@pizzaBP.route('/pizza/edicao/<id>', methods=['POST'])
def edicao_pizza_post(id):
    id_pizza = int(request.form['id_pizza'])
    sabor = str(request.form['sabor'])
    descricao = str(request.form['descricao'])
    valor = request.form['valor'].replace('.', ',').replace(',', '.')
    valor = float(valor)
    url_foto = str(request.form['url_foto'])
    weight = str(request.form['weight'])
    with connection.cursor() as cursor:
        sql = """UPDATE madarah.tb_pizza SET sabor = (%s), descricao = (%s), valor = (%s), url_foto = (%s), weight = (%s) WHERE id_pizza = (%s)"""
        cursor.execute(sql, (sabor, descricao, valor, url_foto, weight, id_pizza))
        connection.commit()
        cursor.close()
        return '/pizzas'


@pizzaBP.route('/pizza/delete/<id>', methods=['GET'])
def delete_pizza_get(id):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM madarah.tb_pizza WHERE id_pizza = " + id
        cursor.execute(sql)
        oi = cursor.fetchone()
        pizza = tuple_to_dict(cursor.description, oi)
    return render_template('excluir_pizza.html', pizza=pizza)
    
@pizzaBP.route('/pizza/delete/<id>', methods=['POST'])
def delete_pizza_post(id):
    with connection.cursor() as cursor: 
        sql = """UPDATE madarah.tb_pizza SET ativo = false WHERE id_pizza = """ + id
        # sql = "DELETE FROM madarah.tb_pizza WHERE id_pizza = " + id
        cursor.execute(sql)
        connection.commit()
        cursor.close()
    return '/pizzas'
