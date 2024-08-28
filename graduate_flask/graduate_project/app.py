from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Task {self.title}>'

@app.route('/')
def task_list():
    tasks = Task.query.all()
    return render_template('article_list.html', tasks=tasks)

@app.route('/task/<int:task_id>')
def task_detail(task_id):
    task = Task.query.get_or_404(task_id)
    return render_template('article_detail.html', task=task)

@app.route('/task/new', methods=['GET', 'POST'])
def task_new():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        completed = 'completed' in request.form
        new_task = Task(title=title, description=description, completed=completed)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('task_detail', task_id=new_task.id))
    return render_template('article_edit.html')

@app.route('/task/<int:task_id>/edit', methods=['GET', 'POST'])
def task_edit(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form['description']
        task.completed = 'completed' in request.form
        db.session.commit()
        return redirect(url_for('task_detail', task_id=task.id))
    return render_template('article_edit.html', task=task)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)