from flask import Flask, request, redirect, url_for, render_template, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Chave para usar sessões e mensagens

# Caminho para o banco de dados SQLite
DB_PATH = 'database.db'

# Função para criar o banco de dados e a tabela
def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        conn.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            rg TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
        ''')
        conn.close()

# Inicializa o banco de dados
init_db()

# Função para obter a conexão com o banco de dados
def get_db():
    conn = sqlite3.connect(DB_PATH)
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        rg = request.form['rg']
        email = request.form['email']
        password = request.form['password']

        conn = get_db()
        try:
            conn.execute('INSERT INTO users (name, address, city, state, rg, email, password) VALUES (?, ?, ?, ?, ?, ?, ?)',
                         (name, address, city, state, rg, email, password))
            conn.commit()
            flash('Cadastro realizado com sucesso!')
            return redirect(url_for('index'))
        except sqlite3.IntegrityError:
            flash('Email já cadastrado!')
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    conn = get_db()
    cursor = conn.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return render_template('welcome.html')
    flash('Email ou senha inválidos!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
