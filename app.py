from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
app = Flask(__name__)

# --- DB setup ---
DB_PATH = os.path.join('/tmp', 'used_mobiles.db')
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS mobiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    color TEXT,
    storage TEXT,
    ram TEXT,
    condition TEXT,
    issues TEXT,
    buy_price INTEGER,
    sell_price INTEGER
)
''')
conn.commit()
conn.close()

# --- Routes ---
@app.route('/')
def index():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM mobiles")
    mobiles = c.fetchall()
    conn.close()
    return render_template('index.html', mobiles=mobiles)

@app.route('/add', methods=['POST'])
def add():
    data = (
        request.form['name'],
        request.form['color'],
        request.form['storage'],
        request.form['ram'],
        request.form['condition'],
        request.form['issues'],
        request.form['buy_price'],
        request.form['sell_price']
    )
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO mobiles (name, color, storage, ram, condition, issues, buy_price, sell_price)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", data)
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM mobiles WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
