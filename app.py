from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
import config

app = Flask(__name__)

# MySQL Config
app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB

mysql = MySQL(app)

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Add Note
@app.route('/add', methods=['POST'])
def add_note():
    data = request.get_json()
    content = data['content']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO notes (content) VALUES (%s)", (content,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Note added'})

# Get Notes
@app.route('/get', methods=['GET'])
def get_notes():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM notes")
    notes = cur.fetchall()
    cur.close()

    return jsonify(notes)

# Delete Note
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_note(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM notes WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Deleted'})

if __name__ == '__main__':
    app.run(debug=True)