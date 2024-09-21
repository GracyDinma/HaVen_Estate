from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)

@app.route('/sign_in', methods=['POST'])
def sign_in():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
    user = cursor.fetchone()

    if user and check_password_hash(user[2], pasword):
        return jsonify({'message': 'Sign-in successful!', 'user_id': user[0]}), 200
    return jsonify({'message': 'Invalid credentials!'}), 401


@app.route('/contact', methods=['POST'])
def contact():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)', (name, email, message))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Message sent successfully!'}), 201


if __name__ == '__main__':
    app.run(debug=True)

