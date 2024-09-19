from flask import Flask, session, request, render_template, url_for, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_mysqldb import MySQL

app = Flask(__name__)
# login_manager = LoginManager()
# login_manager.init_app(app) #Configura app para trabalhar junto com flask-login

#configurações necessárias para usar o mysql:
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_empresa'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = 'megamegadificil'


conexao = MySQL(app)
login_manager = LoginManager()
login_manager.init_app(app) #Configura app para trabalhar junto com flask-login

def get_cursor():
    return conexao.connection.cursor()

def commit_con():
    return conexao.connection.commit()


@login_manager.user_loader #Carregar usuário logado
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def index():
    return render_template('nav/index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
        
        if request.method == 'POST': #metodo post
            matricula = request.form['matricula']
            senha = request.form['senha']
            fun = User.get_by_nome(matricula)
            if fun is None: # Se o login falhar
                flash("Usuário não cadastrado. <a href='" + url_for('cadastro') + "'>Cadastre-se aqui</a>", "error")
                return redirect(url_for('login')) 
            if check_password_hash(fun['fun_senha'], senha):  # Se o usuário for encontrado
                    login_user(User.get(fun['fun_id'])) 
                    return redirect(url_for('dash'))  # Redireciona para a página de filmes
            flash("Senha Incorreta", "error")
            return redirect(url_for('login'))
    
        else:
            return render_template('nav/login.html')

@app.route('/cadastro', methods = ['GET', 'POST'])
def cadastro():
        
        if request.method == 'GET':
            return render_template('nav/cadastro.html')
        else: #Se o método for post:
            matricula = request.form['matricula']
            email = generate_password_hash(request.form['email'])
            senha = generate_password_hash(request.form['senha'])
        if not User.exists(matricula): #se o usuário não tiver cadastro
            user = User(fun_matricula = matricula, fun_email = email, fun_senha = senha)
            user.save()
            login_user(user)
            flash('Cadastro Realizado!', 'success')
            return redirect(url_for('dash'))
        else:
            flash('usuário já existe!', 'error')

@app.route('/inicio')
@login_required
def dash():
    usu_exe = str(current_user._id)
    cursor = get_cursor()
    cursor.execute("SELECT exe_id,exe_nome,exe_descricao,exe_fun_id FROM tb_exercicios WHERE exe_fun_id = %s", (usu_exe,))
    exercicios = cursor.fetchall()
    print(exercicios)
    
    return render_template('nav/dash.html', exercicios = exercicios)

@app.route('/cadastrar-exercicio', methods=['GET', 'POST'])
@login_required
def novo_exe():
     
     if request.method == 'POST':
          exe_nome = request.form['nome']
          exe_descricao = request.form['descricao']
          usu_exe = current_user._id

          cursor = get_cursor()
          cursor.execute("INSERT INTO tb_exercicios(exe_nome, exe_descricao, exe_fun_id) VALUES (%s, %s, %s)", (exe_nome, exe_descricao, usu_exe))
          commit_con()
          return redirect(url_for('dash'))


     return render_template('nav/new.html')

@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    flash('Logout Realizado', 'success')
    return redirect(url_for('index'))