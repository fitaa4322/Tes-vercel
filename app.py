from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # diperlukan untuk flash message

# Koneksi database via PyMySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:BzUobQyvRWDoeVzGQpDIvsRpdkfwqIns@shinkansen.proxy.rlwy.net:58092/railway'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        if not name or not email:
            flash("Nama dan Email harus diisi!")
            return redirect('/add')

        try:
            new_user = User(name=name, email=email)
            db.session.add(new_user)
            db.session.commit()
            flash("Data berhasil ditambahkan!")
            return redirect('/')
        except Exception as e:
            flash(f"Error saat menambahkan data: {str(e)}")
            return redirect('/add')

    return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True)
