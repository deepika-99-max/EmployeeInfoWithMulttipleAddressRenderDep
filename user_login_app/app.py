from flask import Flask, render_template, request, redirect, session, url_for
from models import db, User, Address
from config import Config
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

#@app.before_first_request
#def create_tables():
#    db.create_all()



@app.route('/')
def index():
    return render_template('index.html')


#@app.route('/')
#def home():
#    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        user = User(
            name=data['name'],
            phone=data['phone'],
            email=data['email'],
            joining_date=datetime.strptime(data['joining_date'], "%Y-%m-%d"),
            username=data['username'],
            password=data['password']
        )
        db.session.add(user)
        db.session.flush()
        for addr in request.form.getlist('address'):
            db.session.add(Address(line=addr, user_id=user.id))
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username'], password=request.form['password']).first()
        if user:
            session['user_id'] = user.id
            return redirect('/dashboard')
        return 'Invalid credentials'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', user=user)

@app.route('/edit_address/<int:address_id>', methods=['GET', 'POST'])
def edit_address(address_id):
    address = Address.query.get_or_404(address_id)
    if request.method == 'POST':
        address.line = request.form['line']
        db.session.commit()
        return redirect('/dashboard')
    return render_template('edit_address.html', address=address)

@app.route('/delete_address/<int:address_id>')
def delete_address(address_id):
    address = Address.query.get_or_404(address_id)
    db.session.delete(address)
    db.session.commit()
    return redirect('/dashboard')

if __name__ == '__main__':
    app.secret_key = app.config['SECRET_KEY']
    app.run(debug=True)
