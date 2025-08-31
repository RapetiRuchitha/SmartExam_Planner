from flask import Flask, render_template, request, redirect, url_for, flash
from config import get_db_connection
from matrix2 import run, write, missing, read
import pandas as pd  # Ensure pandas is imported

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a secure key

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = request.form.get('user')
        password = request.form.get('psw')
        if user == "admin" and password == "admin":
            return redirect(url_for('admin'))
        else:
            error = "Invalid user or password!"
    return render_template("login.html", error=error)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/admin")
def admin():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rooms")
    data = cursor.fetchall()
    conn.close()
    return render_template("admin.html", data=data)

@app.route("/addroom", methods=['GET', 'POST'])
def add_room():
    error = None
    if request.method == 'POST':
        room_no = request.form['room_no']
        row = request.form['row']
        col = request.form['col']
        seat = request.form['seat']

        if int(seat) > int(row) * int(col):
            error = "Invalid number of seats."
        else:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT room_no FROM rooms WHERE room_no=%s", (room_no,))
            existing_room = cursor.fetchone()
            if existing_room:
                error = f"Room {room_no} already exists."
            else:
                cursor.execute("INSERT INTO rooms (room_no, row_count, col_count, total_seats) VALUES (%s, %s, %s, %s)",
                               (room_no, row, col, seat))
                conn.commit()
                flash(f"Room {room_no} added successfully!", "success")
            cursor.close()
            conn.close()
    return render_template("addroom.html", error=error)

@app.route("/Generate", methods=['GET', 'POST'])
def generate():
    error = None
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT room_no FROM rooms")
    room_numbers = cursor.fetchall()
    conn.close()
    
    if request.method == 'POST':
        room_no = request.form['room']
        it_start, it_end = int(request.form['it_start']), int(request.form['it_end'])
        ec_start, ec_end = int(request.form['ec_start']), int(request.form['ec_end'])
        el_start, el_end = int(request.form['el_start']), int(request.form['el_end'])
        
        r_missing = list(map(int, request.form['missing'].split())) if request.form['missing'] else []

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT row_count, col_count, total_seats FROM rooms WHERE room_no = %s", (room_no,))
        room_data = cursor.fetchone()
        conn.close()
        
        if not room_data:
            error = "Room not found."
        else:
            row, col, seat = room_data
            it_list = missing(r_missing, list(range(it_start, it_end + 1)))
            ec_list = missing(r_missing, list(range(ec_start, ec_end + 1)))
            el_list = missing(r_missing, list(range(el_start, el_end + 1)))

            if len(it_list) + len(ec_list) + len(el_list) <= seat:
                data = run(el_list, ec_list, it_list, row, col)
                
                if isinstance(data, list):  # Ensure data is a DataFrame
                    data = pd.DataFrame(data)

                write(data, room_no)
                flash(f"Seating arrangement for Room {room_no} generated!", "success")
            else:
                error = f"Total students exceed seat limit ({seat})."

    return render_template("generate.html", room_no=room_numbers, error=error)

@app.route('/result', methods=['GET', 'POST'])
def show():
    data = None
    filename = None
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT room_no FROM rooms")
    room_numbers = cursor.fetchall()
    conn.close()

    if request.method == 'POST':
        room_no = request.form['room']
        df = read(room_no)
        
        if df is None or df.empty:  # Check for valid DataFrame
            flash(f"No seating arrangement found for Room {room_no}.", "warning")
        else:
            data = df.to_html()
            filename = f'/static/excel/{room_no}.xlsx'

    return render_template("show_result.html", data=data, room_no=room_numbers, filename=filename)

@app.route('/delete/<id>')
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM rooms WHERE room_no=%s", (id,))
    conn.commit()
    conn.close()
    flash(f"Room {id} deleted successfully!", "danger")
    return redirect(url_for('admin'))

if __name__ == "__main__":
    app.run(debug=True)
