import os
import tempfile

import unittest

import todos


class TodosTestCase(unittest.TestCase):

  def addTodo(self, text='A wonderful Todo', priority=0, completed=False):
    return self.app.post('/create_todo', data=dict(
      todo_text=text,
      priority=priority,
      completed=completed
    ), follow_redirects=True)

  def setUp(self):
    self.db_fd, todos.app.config['DATABASE'] = tempfile.mkstemp()
    self.app = todos.app.test_client()
    todos.init_db()

  def tearDown(self):
    os.close(self.db_fd)
    os.unlink(todos.app.config['DATABASE'])

  def test_empty_db(self):
    response = self.app.get('/')
    assert 'No todos yet!' in response.data

  def test_new_todo(self):
    response = self.addTodo(text='A test todo')
    assert 'A test todo' in response.data

def test_

if __name__ == '__main__':
  unittest.main()