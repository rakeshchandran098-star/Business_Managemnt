from flask import Flask, render_template, request, redirect, url_for, session, flash

from data.data import employees, products, customers, sales

app = Flask(__name__)

app.secret_key = "business_management_secret"


# LOGIN

@app.route('/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "admin123":

            session['user'] = username

            return redirect(url_for('dashboard'))

        flash("Invalid username or password")

    return render_template('login.html')


# DASHBOARD

@app.route('/dashboard')
def dashboard():

    if 'user' not in session:
        return redirect(url_for('login'))

    total_salary = sum(emp['salary'] for emp in employees)

    total_revenue = sum(sale['amount'] for sale in sales)

    return render_template(
        'dashboard.html',
        employees=employees,
        products=products,
        customers=customers,
        sales=sales,
        total_salary=total_salary,
        total_revenue=total_revenue
    )


# EMPLOYEE MANAGEMENT

@app.route('/employees', methods=['GET', 'POST'])
def employee_management():

    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':

        new_employee = {

            "id": max([e['id'] for e in employees], default=0) + 1,

            "name": request.form['name'],

            "department": request.form['department'],

            "salary": float(request.form['salary'])

        }

        employees.append(new_employee)

        flash("Employee added successfully")

        return redirect(url_for('employee_management'))

    search = request.args.get('search', '').lower()

    filtered_employees = [
        emp for emp in employees
        if search in emp['name'].lower()
    ]

    return render_template(
        'employees.html',
        employees=filtered_employees
    )


# DELETE EMPLOYEE

@app.route('/delete_employee/<int:id>')
def delete_employee(id):

    if 'user' not in session:
        return redirect(url_for('login'))

    employees[:] = [e for e in employees if e['id'] != id]

    flash("Employee deleted successfully")

    return redirect(url_for('employee_management'))


# PRODUCT MANAGEMENT

@app.route('/products', methods=['GET', 'POST'])
def product_management():

    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':

        new_product = {

            "id": max([p['id'] for p in products], default=0) + 1,

            "name": request.form['name'],

            "category": request.form['category'],

            "price": float(request.form['price']),

            "stock": int(request.form['stock'])

        }

        products.append(new_product)

        flash("Product added successfully")

        return redirect(url_for('product_management'))

    return render_template('products.html', products=products)


# DELETE PRODUCT

@app.route('/delete_product/<int:id>')
def delete_product(id):

    if 'user' not in session:
        return redirect(url_for('login'))

    products[:] = [p for p in products if p['id'] != id]

    flash("Product deleted successfully")

    return redirect(url_for('product_management'))


# CUSTOMER MANAGEMENT

@app.route('/customers', methods=['GET', 'POST'])
def customer_management():

    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':

        new_customer = {

            "id": max([c['id'] for c in customers], default=0) + 1,

            "name": request.form['name'],

            "city": request.form['city']

        }

        customers.append(new_customer)

        flash("Customer added successfully")

        return redirect(url_for('customer_management'))

    return render_template('customers.html', customers=customers)


# SALES

@app.route('/sales', methods=['GET', 'POST'])
def sales_management():

    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':

        product_name = request.form['product']

        quantity = int(request.form['quantity'])

        product = next(
            (p for p in products if p['name'] == product_name),
            None
        )

        if product is None:
            flash("Product not found")

        elif quantity <= 0 or quantity > product['stock']:
            flash("Invalid quantity or insufficient stock")

        else:

            amount = product['price'] * quantity

            product['stock'] -= quantity

            new_sale = {

                "id": max([s['id'] for s in sales], default=0) + 1,

                "product": product_name,

                "quantity": quantity,

                "amount": amount

            }

            sales.append(new_sale)

            flash("Sale recorded successfully")

        return redirect(url_for('sales_management'))

    return render_template(
        'sales.html',
        sales=sales,
        products=products
    )


# LOGOUT

@app.route('/logout')
def logout():

    session.clear()

    return redirect(url_for('login'))


if __name__ == '__main__':

    app.run(debug=True)