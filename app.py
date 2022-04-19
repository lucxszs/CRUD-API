from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:9799@localhost/cadastro'

db = SQLAlchemy(app)

class Pessoa(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    nome = db.Column(db.String(50))
    sobrenome = db.Column(db.String(50))
    email = db.Column(db.String(50))
    nacionalidade = db.Column(db.String(30))
    cep = db.Column(db.Integer)
    estado = db.Column(db.String(30))
    cidade = db.Column(db.String(30))
    logradouro = db.Column(db.String(50))
    email = db.Column(db.String(50))
    telefone = db.Column(db.Integer)
    
    def to_json(self):
        return {"id": self.id, "nome": self.nome, "sobrenome": self.sobrenome,"email": self.email, "nacionalidade": self.nacionalidade,"cep": self.cep,"estado": self.estado, "cidade": self.cidade, "logradouro": self.logradouro, "email": self.email, "telefone": self.telefone}
    
#Selecionar Tudo
@app.route("/usuarios", methods=["GET"])
def seleciona_usuarios():
    usuarios_objetos = Pessoa.query.all()
    usuarios_json = [pessoa.to_json() for pessoa in usuarios_objetos]

    return gera_response(200, "usuarios", usuarios_json)

#Selecionar Individual
@app.route("/usuario/<id>")
def seleciona_usuario(id):
    usuario_objeto = Pessoa.query.filter_by(id=id).first()
    usuario_json = usuario_objeto.to_json()

    return gera_response(200, "usuario", usuario_json)

#Cadastrar
@app.route("/usuario", methods=["POST"])
def cria_usuario():
    body = request.get_json()

    try:
        usuario = Pessoa(nome=body["nome"], sobrenome=body["sobrenome"], nacionalidade=body["nacionalidade"], cep=body["cep"], estado=body["estado"], cidade=body["cidade"], logradouro=body["logradouro"], email=body["email"], telefone=body["telefone"])
        db.session.add(usuario)
        db.session.commit()
        return gera_response(201, "usuario", usuario.to_json(), "Criado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400,"usuario", {}, "Erro ao cadastrar")


# Atualizar
@app.route("/usuario/<id>", methods=["PUT"])
def atualiza_usuario(id):
    usuario_objeto = Pessoa.query.filter_by(id=id).first()
    body = request.get_json()

    try:
        if('nome' in body):
            usuario_objeto.nome = body['nome']
        if('sobrenome' in body):
            usuario_objeto.sobrenome = body['sobrenome']
        if('nacionalidade' in body):
            usuario_objeto.nacionalidade = body['nacionalidade']
        if('cep' in body):
            usuario_objeto.cep = body['cep']
        if('estado' in body):
            usuario_objeto.estado = body['estado']
        if('cidade' in body):
            usuario_objeto.cidade = body['cidade']
        if('logradouro' in body):
            usuario_objeto.logradouro = body['logradouro']
        if('email' in body):
            usuario_objeto.email = body['email']
        if('telefone' in body):
            usuario_objeto.telefone = body['telefone']
        
        db.session.add(usuario_objeto)
        db.session.commit()
        return gera_response(200, "usuario", usuario_objeto.to_json(), "Atualizado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "usuario", {}, "Erro ao atualizar")

# Deletar
@app.route("/usuario/<id>", methods=["DELETE"])
def deleta_usuario(id):
    usuario_objeto = Pessoa.query.filter_by(id=id).first()

    try:
        db.session.delete(usuario_objeto)
        db.session.commit()
        return gera_response(200, "usuario", usuario_objeto.to_json(), "Deletado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "usuario", {}, "Erro ao deletar")

def gera_response(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo
    
    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json")

def home(request):
    return render(request, 'index.html')

app.run()
