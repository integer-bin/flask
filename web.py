from flask import Flask, request, render_template, redirect, url_for, session, flash
import socket
from flask_mysqldb import MySQL
import MySQLdb.cursors


app = Flask(__name__)
app.secret_key = 'wjdtnqls'

# MySQL 설정
app.config['MYSQL_HOST'] = 'db.rapa.local'
#app.config['MYSQL_PORT'] = 3306  # MySQL 포트 (기본값)
app.config['MYSQL_USER'] = 'frodo'
app.config['MYSQL_PASSWORD'] = 'frodo5020!!'
app.config['MYSQL_DB'] = 'frodo'

mysql = MySQL(app)

@app.route('/')
def index():        # 추후 로그인 페이지 구현

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        
        if account:
            flash('Account already exists!')
            
        elif not username or not password:
            flash('Please fill out the form!')
            #return redirect(url_for('login'))
        else:
            cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
            mysql.connection.commit()
            flash('You have successfully registered!')
            
    elif request.method == 'POST':
        flash('Please fill out the form!')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        
        if account:
            session['username'] = username
            cursor.close()       
            return redirect(url_for('welcome'))
        else:
            cursor.close() 
            flash('Incorrect username/password!')
        
    return render_template('login.html')

@app.route('/welcome')
def welcome():
    if 'username' not in session:
        return redirect(url_for('login.html'))
       
    client_ip = request.remote_addr
    server_ip = request.host.split(':')[0]
    server_name = socket.gethostname()

    return render_template('welcome.html', username=session['username'], client_ip=client_ip, server_name=server_name, server_ip=server_ip)   

@app.route('/logout')
def logout():
    session.pop('username', None)
    
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
