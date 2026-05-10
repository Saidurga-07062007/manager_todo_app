from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Database Setup
def init_db():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT,
            priority TEXT,
            status TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# Home Page
@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()

    conn.close()

    return render_template('index.html', tasks=tasks)

# Add Task
@app.route('/add', methods=['POST'])
def add_task():

    task = request.form['task']
    priority = request.form['priority']

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute('''
        INSERT INTO tasks(task, priority, status)
        VALUES (?, ?, ?)
    ''', (task, priority, 'Pending'))

    conn.commit()
    conn.close()

    return redirect('/')

# Complete Task
@app.route('/complete/<int:id>')
def complete_task(id):

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute('''
        UPDATE tasks
        SET status = 'Completed'
        WHERE id = ?
    ''', (id,))

    conn.commit()
    conn.close()

    return redirect('/')

# Delete Task
@app.route('/delete/<int:id>')
def delete_task(id):

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute('DELETE FROM tasks WHERE id = ?', (id,))

    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)