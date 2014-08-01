# Python imports
import os
from sqlite3 import dbapi2 as sqlite3

# 3rd party imports
from flask import Flask, g, request, render_template, redirect, url_for

# Local Imports

## END IMPORTS

app = Flask(__name__)

app.config.update(dict(
  DATABASE=os.path.join(app.root_path, 'todos.db'),
  DEBUG=True,
  SECRET_KEY='todos key'
))

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    with app.app_context():
      db = get_db()
      with app.open_resource('create_tables.sql', mode='r') as f:
          db.cursor().executescript(f.read())
      db.commit()

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context."""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def list_todos():
  db = get_db()
  cur = db.execute('select todo_text, priority, completed from todos order by id desc')
  todos = cur.fetchall()
  return render_template('index.html', todos=todos)

@app.route('/add_todo')
def add_todo():
  db = get_db()
  db.execute('insert into todos (todo_text, priority, completed) values (?,?,?)',
    [request.form['title'], request.form['text']])
  db.commit()
  flash('New todo was created!')
  return redirect(url_for('list_todos'))


@app.route('/create_todo', methods=['POST'])
def create_todo():
  if request.method == 'POST':
    todo_text = request.form['todo_text']
    priority = request.form['priority']
    completed = request.form['completed']
    db = get_db()
    db.execute('insert into todos (todo_text, priority, completed) values (?, ?, ?)',
               [todo_text, priority, completed])
    db.commit()
  return redirect(url_for('list_todos'))

  
if __name__ == '__main__':
    app.run()


