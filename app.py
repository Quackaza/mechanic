from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Function to add entry to the database
def add_entry(customer_name, phone_number, license_plate, make, model, km, date, service_history, price):
    conn = sqlite3.connect('mechanic_shop.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS entries
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 customer_name TEXT,
                 phone_number TEXT,
                 license_plate TEXT,
                 make TEXT,
                 model TEXT,
                 km TEXT,
                 date TEXT,
                 service_history TEXT,
                 price TEXT)''')
    c.execute("INSERT INTO entries (customer_name, phone_number, license_plate, make, model, km, date, service_history, price) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (customer_name, phone_number, license_plate, make, model, km, date, service_history, price))
    conn.commit()
    conn.close()

# Function to display search result
def search_exact(search_text):
    conn = sqlite3.connect('mechanic_shop.db')
    c = conn.cursor()
    c.execute("SELECT * FROM entries WHERE license_plate = ?", (search_text,))
    rows = c.fetchall()
    conn.close()
    return rows

# Function to display all licenses and customer names
def display_all_licenses():
    conn = sqlite3.connect('mechanic_shop.db')
    c = conn.cursor()
    c.execute("SELECT id, license_plate, phone_number, make, model, GROUP_CONCAT(DISTINCT customer_name) FROM entries GROUP BY license_plate")
    rows = c.fetchall()
    conn.close()
    return rows

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        phone_number = request.form['phone_number']
        license_plate = request.form['license_plate']
        make = request.form['make']
        model = request.form['model']
        km = request.form['km']
        date = request.form['date']
        service_history = request.form['service_history']
        price = request.form['price']
        add_entry(customer_name, phone_number, license_plate, make, model, km, date, service_history, price)
        flash('Entry added successfully', 'success')
        return redirect(url_for('home'))

@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        search_text = request.form['search_text']
        rows = search_exact(search_text)
        if rows:
            return render_template('search_result.html', rows=rows)
        else:
            flash('No car found with the given license plate', 'danger')
            return redirect(url_for('home'))

@app.route('/display_all')
def display_all():
    rows = display_all_licenses()
    return render_template('display_all.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
