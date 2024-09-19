from flask import Flask
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL


app = Flask(__name__)
conexao = MySQL(app)


#configurações necessárias para usar o mysql:
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_empresa'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

def get_conexao():
    return conexao.connection.cursor() #conexao com o banco

def commit_con():
    return conexao.connection.commit() #fazer commits



class User(UserMixin): #definindo a classe usuario
    _hash : str
    def __init__(self, **kwargs):
        self._id = None

        if 'fun_id' in kwargs.keys(): #id do usuario
            self._id = kwargs.keys()
        if 'fun_matricula' in kwargs.keys():
            self._nome = kwargs['fun_matricula'] #nome do usuario
        if 'fun_email' in kwargs.keys():
            self._email = kwargs['fun_email'] #email do usuario
        if 'fun_senha' in kwargs.keys():
            self._senha = kwargs['fun_senha'] #senha(hash) do usuario
        
    # 5 - sobresrever get id do UserMixin
    def get_id(self):
        return str(self._id)
    
    # ----------métodos para manipular o banco--------------#
    def save(self):   #Salvar os dados  
        cursor = get_conexao() 
        cursor.execute("INSERT INTO tb_funcionarios(fun_matricula, fun_email, fun_senha) VALUES (%s, %s, %s)", (self._nome, self._email, self._senha))
        # salva o id no objeto recem salvo no banco
        self._id = cursor.lastrowid
        commit_con()
        cursor.close()
        return True
    
    @classmethod
    def get(cls,user_id): #pegar os dados de um usuário
        cursor = get_conexao()
        cursor.execute("SELECT * FROM tb_funcionarios WHERE fun_id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        
        if user:
            loaduser = User(matricula=user['fun_matricula'] , senha=user['fun_senha'])
            loaduser._id = user['fun_id']
            return loaduser
        else:
            return None
    
    @classmethod
    def exists(cls, matricula): #Verificar se usário existe
        cursor = get_conexao()
        cursor.execute("SELECT * FROM tb_funcionarios WHERE fun_matricula = %s", (matricula,))
        user = cursor.fetchone()
        cursor.close()
        if user: 
            return True
        else:
            return False
    
    @classmethod
    def all(cls): #Pegar todos os dados
        cursor = get_conexao
        cursor.execute("SELECT fun_id, fun_matricula, fun_email FROM tb_funcionarios")
        users = cursor.fetchall()
        cursor.close()
        return users
    
    @classmethod
    def get_by_nome(cls,matricula): #pegar usuário pelo nome
        cursor = get_conexao()
        cursor.execute("SELECT fun_id,fun_matricula,fun_email,fun_senha FROM tb_funcionarios WHERE fun_matricula = %s", (matricula,))
        user = cursor.fetchone()
        cursor.close()
        return user