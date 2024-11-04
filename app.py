from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google
import pymysql
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='Sworaj@1235',
        database='leave_management_system'
    )

app = Flask(__name__)
google_bp = make_google_blueprint(client_id='YOUR_GOOGLE_CLIENT_ID', client_secret='YOUR_GOOGLE_CLIENT_SECRET', redirect_to='google_login')
app.register_blueprint(google_bp, url_prefix='/google_login')
app.secret_key = 'this_is_a_random_secret_key_12345'

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/employee_dashboard')
def employee_dashboard():
    return render_template('employee_dashboard.html')

@app.route('/manager_dashboard')
def manager_dashboard():
    return render_template('manager_dashboard.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            return "Email and password are required", 400

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT password, role FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        # Here you would typically use bcrypt or another library to check hashed passwords
        if user and user[0] == password:  # This should be hashed password comparison
            role = user[1]
            if role == "employee":
                return redirect(url_for('employee_dashboard'))
            elif role == "manager":
                return redirect(url_for('manager_dashboard'))
        return "Invalid credentials", 401  # Provide a more user-friendly message

    return render_template('login.html')
@app.route('/google_login')
def google_login():
    if not google.authorized:
        return redirect(url_for('google.login'))
    
    resp = google.get('/plus/v1/people/me')
    assert resp.ok, resp.text
    email = resp.json()['emails'][0]['value']

    # Logic to check if the user exists in your database, if not, create a new user.
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT role FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()

    if user:
        role = user[0]
        if role == "employee":
            return redirect(url_for('employee_dashboard'))
        elif role == "manager":
            return redirect(url_for('manager_dashboard'))
    else:
        # Optionally, you could redirect to a registration page if user doesn't exist
        return "User not found, please register", 404

    return redirect(url_for('home'))
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        employee_name = request.form.get('employee_name')
        role = request.form.get('role')

        # Validate the input
        if not email or not password or not employee_name or not role:
            return "All fields are required", 400

        # Example of email format validation (you can use regex for a better check)
        if "@" not in email:
            return "Invalid email format", 400

        connection = get_db_connection()
        cursor = connection.cursor()
        
        try:
            # Insert the new user into the users table
            cursor.execute("INSERT INTO users (email, password, employee_name, role) VALUES (%s, %s, %s, %s)", 
                           (email, password, employee_name, role))
            connection.commit()
        except Exception as e:
            connection.rollback()
            return str(e), 400  # Handle duplicate email or other errors

        cursor.close()
        connection.close()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/leave_request', methods=['GET', 'POST'])
def leave_request():
    if request.method == 'POST':
        employee_id = request.form['employee-id']
        employee_name = request.form['employee-name']
        leave_type = request.form['leave-type']
        start_date = request.form['start-date']
        end_date = request.form['end-date']
        reason = request.form['reason']
        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            query = """INSERT INTO leave_requests (employee_id, employee_name, leave_type, start_date, end_date, reason, status)
                       VALUES (%s, %s, %s, %s, %s, %s, 'Pending')"""
            values = (employee_id, employee_name, leave_type, start_date, end_date, reason)
            cursor.execute(query, values)
            connection.commit()
            return redirect(url_for('employee_dashboard'))
            
        except pymysql.MySQLError as e:
            print(f"Error: {e}")
            connection.rollback()  
            return "Failed to submit leave request", 500
        finally:
            cursor.close()
            connection.close()
    
    return render_template('leave_request.html')

@app.route('/leave_approve', methods=['GET', 'POST'])
def leave_approve():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM leave_requests")
    requests = cursor.fetchall()
    cursor.close()
    connection.close()

    if request.method == 'POST':
        employee_id = request.form['employee_id']
        action = request.form['action']

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            if action == "approve":
                cursor.execute("SELECT * FROM leave_requests WHERE employee_id = %s", (employee_id,))
                leave_request = cursor.fetchone()

                if leave_request:
                    query_insert = """
                        INSERT INTO approved_leave (employee_id, employee_name, leave_type, start_date, end_date, reason)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(query_insert, (
                        leave_request[0],  # employee_id
                        leave_request[1],  # employee_name
                        leave_request[2],  # leave_type
                        leave_request[3],  # start_date
                        leave_request[4],  # end_date
                        leave_request[5]   # reason
                    ))

                    cursor.execute("DELETE FROM leave_requests WHERE employee_id = %s", (employee_id,))

            elif action == "reject":
                cursor.execute("DELETE FROM leave_requests WHERE employee_id = %s", (employee_id,))
            connection.commit()

        except pymysql.MySQLError as err:
            print(f"Error: {err}")
            connection.rollback()  

        finally:
            cursor.close()
            connection.close()

        return redirect(url_for('leave_approve'))

    return render_template('leave_approve.html', requests=requests)

@app.route('/calendar')
def calendar():
    return render_template('calendar.html') 

@app.route('/leave_balance')
def leave_balance():
    return render_template('leave_balance.html')

@app.route('/api/leave_balance')
def api_leave_balance():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    total_leave = 100  

    query = """
        SELECT employee_id, employee_name, SUM(DATEDIFF(end_date, start_date)) AS total_days_taken
        FROM approved_leave
        GROUP BY employee_id, employee_name
    """
    cursor.execute(query)
    leave_data = cursor.fetchall()

    leave_balances = []
    for leave in leave_data:
        days_taken = leave['total_days_taken'] if leave['total_days_taken'] else 0
        remaining_leave = total_leave - days_taken
        leave_balances.append({
            'employee_id': leave['employee_id'],
            'employee_name': leave['employee_name'],
            'total_leave': total_leave,
            'current_leave': days_taken,
            'remaining_leave': remaining_leave
        })

    cursor.close()
    conn.close()
    return jsonify(leave_balances)

@app.route('/api/leave_data')
def api_leave_data():
    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT employee_name, start_date, end_date FROM approved_leave")
    leave_data = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(leave_data)
@app.errorhandler(500)
def internal_error(error):
    return "An internal error occurred: {}".format(error), 500
@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify(success=False, message="Method Not Allowed."), 405



if __name__ == '__main__':
    app.run(debug=True)
