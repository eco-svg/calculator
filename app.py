from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS calculations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expression TEXT,
            result TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    expression = data['expression']

    try:
        result = str(eval(expression))
    except:
        result = "Error"

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO calculations (expression, result) VALUES (?, ?)", (expression, result))
    conn.commit()
    conn.close()

    return jsonify({'result': result})


@app.route('/history')
def history():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM calculations ORDER BY id DESC LIMIT 10")
    data = c.fetchall()
    conn.close()

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)