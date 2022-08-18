from flask import Flask, Response, Request
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/crud'
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    nome = db.Column(db.String(50))
    email = db.Column(db.String(100))

    def to_json(self):
        return {"id": self.id, "nome": self.nome, "email": self.email}

@app.route("/usuarios", methods=["GET"])
def seleciona_usuarios():
    usuario_classe = Usuario.query.all()
    usuario_json = [usuario.to_json() for usuario in usuario_classe]
    return gera_resposta(200, "usuarios", usuario_json,)

def gera_resposta(status, ndc, conteudo, mensagem=False):
    body = {}
    body = [ndc] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json")

@app.route("/usuario/<id>", methods=["GET"])
def seleciona_usuario(id):
    usuario_class = Usuario.query.filter_by(id=id).first()
    usuario_json = usuario_class.to_json()

    return gera_resposta(200, "usuario", usuario_json)

@app.route("/usuario", methods=["POST"])
def criar_usuario():
    body = request.get_json()
    try:
         usuario = Usuario(nome=body["nome"], email= body["email"])
         db.session.add (usuario)
         db.session.commit()
         return gera_resposta(201, "usuario", usuario.to_json(), "Criado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, "usuario", {}, "Erro!")

@app.route("/usuario/<id>", methods=["PUT"])
def att_usuario(id):
    usuario_class = Usuario.quary.filter_by(id=id).fist()
    body = request.get_json()
    
    try:
        if('nome' in body):
            usuario_class.nome = body['nome']
        if('email' in body):
            usuario_class.email = body['email']
        db.session.add(usuario_class)
        db.session.commit()
        return gera_resposta(200, "usuario", usuario.to.json(), "Atualizado")
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, "usuario", {}, "Houve um erro!")
@app.route("/usuario/<id>", methods=["DELETE"])
def del_usuario(id):
    usuario_class = Usuario.quary.filter_by(id=id).fist()
    try:
        db.session.delete(usuario_class)
        db.session,commit()
        return gera_resposta (200, "usuario", usuario.object.to_json(), "Usuario Deletado")
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, "usuario", {}, "Houve um erro")

app.run()
