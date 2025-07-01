from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
db = SQLAlchemy(app)

# Employee Model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)

# Home Page - List + Add Employee
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        new_emp = Employee(
            name=request.form['name'],
            role=request.form['role'],
            city=request.form['city']
        )
        db.session.add(new_emp)
        db.session.commit()
        return redirect('/')
    employees = Employee.query.all()
    return render_template('home.html', employees=employees)

# Edit Employee
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    emp = Employee.query.get_or_404(id)
    if request.method == 'POST':
        emp.name = request.form['name']
        emp.role = request.form['role']
        emp.city = request.form['city']
        db.session.commit()
        return redirect('/')
    return render_template('edit.html', emp=emp)

# Delete Employee
@app.route('/delete/<int:id>')
def delete(id):
    emp = Employee.query.get_or_404(id)
    db.session.delete(emp)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)