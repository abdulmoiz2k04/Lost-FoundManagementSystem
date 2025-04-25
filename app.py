from flask import Flask, request, render_template, redirect
import mysql
from db_config import connect_db
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secret123'  # Required for session

@app.route('/')
def index():
    query = request.args.get('q', '')
    status_filter = request.args.get('status', '')

    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    sql = """
        SELECT * FROM Items
        WHERE (%s = '' OR title LIKE %s OR description LIKE %s OR category LIKE %s)
          AND (%s = '' OR status = %s)
        ORDER BY date_reported DESC
    """
    values = (query, f"%{query}%", f"%{query}%", f"%{query}%", status_filter, status_filter)

    cursor.execute(sql, values)
    items = cursor.fetchall()
    conn.close()
    return render_template('index.html', items=items)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Users (name, email, password) VALUES (%s, %s, %s)", 
                           (name, email, password))
            conn.commit()
        except mysql.connector.Error as err:
            return f"Error: {err}"
        finally:
            conn.close()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['user_id']
            session['name'] = user['name']
            return redirect('/')
        else:
            return "Invalid login"
    return render_template('login.html')

@app.route('/report', methods=['GET', 'POST'])
def report_item():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']
        category = request.form['category']
        location = request.form['location']
        contact = request.form['contact']
        user_id = session['user_id']

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Items (user_id, title, description, status, category, location, date_reported, contact)
            VALUES (%s, %s, %s, %s, %s, %s, CURDATE(), %s)
        """, (user_id, title, description, status, category, location, contact))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('report.html')

@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    if not session.get('user_id'):
        return redirect('/login')

    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    # Check if user owns the item
    cursor.execute("SELECT * FROM Items WHERE item_id = %s AND user_id = %s", 
                   (item_id, session['user_id']))
    item = cursor.fetchone()
    if not item:
        conn.close()
        return "Not authorized"

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']
        category = request.form['category']
        location = request.form['location']
        contact = request.form['contact']

        cursor.execute("""
            UPDATE Items 
            SET title=%s, description=%s, status=%s, category=%s, location=%s, contact=%s 
            WHERE item_id=%s
        """, (title, description, status, category, location, contact, item_id))
        conn.commit()
        conn.close()
        return redirect('/')
    
    conn.close()
    return render_template('edit.html', item=item)

@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    if not session.get('user_id'):
        return redirect('/login')

    conn = connect_db()
    cursor = conn.cursor()

    # Only delete if the item belongs to the user
    cursor.execute("DELETE FROM Items WHERE item_id = %s AND user_id = %s", 
                   (item_id, session['user_id']))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/claim/<int:item_id>')
def claim(item_id):
    if not session.get('user_id'):
        return redirect('/login')

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE Items SET status = 'claimed' WHERE item_id = %s", (item_id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
