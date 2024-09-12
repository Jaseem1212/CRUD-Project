from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    active = db.Column(db.Boolean, default=True)


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    users = User.query.all()
    return render_template('user_list.html', users=users)


@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        active = request.form.get('active') == 'on'

        new_user = User(username=username, password=password, active=active)
        db.session.add(new_user)
        db.session.commit()
        flash("User added successfully!")
        return redirect(url_for('index'))

    return render_template('user_form.html', action="Add")


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.password = request.form['password']
        user.active = request.form.get('active') == 'on'

        db.session.commit()
        flash("Updated successfully!")
        return redirect(url_for('index'))

    return render_template('user_form.html', user=user, action="Edit")


@app.route('/delete/<int:id>')
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash("Deleted successfully!")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
