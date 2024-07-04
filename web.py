from flask import Flask, request, render_template
import socket
import mysql.connector


app = Flask(__name__)


@app.route('/')
def index():        # 추후 로그인 페이지 구현

    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    client_ip = request.remote_addr
    server_name = socket.gethostname()
    server_ip = socket.gethostbyname(server_name)
    
    return render_template('dashboard.html', client_ip=client_ip, server_name=server_name, server_ip=server_ip)


if __name__ == '__main__':
    app.run(debug=True)
