from flask import Flask, request, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Initialize MySQL connection
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="narayanan@123",
    database="flask"
)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
    else:
        username = request.args.get('username')
        password = request.args.get('password')
        
    if username and password:
        cursor = db_connection.cursor()
        
        sql = "SELECT role FROM login WHERE username = %s AND password = %s"
        cursor.execute(sql, (username, password))
        role = cursor.fetchone()
        
        cursor.close()
        
        if role:
            print("Role Retrieved from Database:", role[0])  # Debugging statement
            if role[0] == 'student':
                return render_template('student.html')
            elif role[0] == 'librarian':
                return render_template('librarian.html')
            elif role[0] == 'admin':
                return render_template('admin_page.html')
            elif role[0] == 'faculty':
                return render_template('faculty.html')
            elif role[0] == "teacher":
                return render_template('teacher.html')
            else:
                return "Unknown role"
        else:
            print("Invalid username or password")  # Debugging statement
            return "Invalid username or password"
    
    return render_template('login_trial.html')

@app.route('/appl/', methods=['GET', 'POST'])
def appl():
    cursor = db_connection.cursor()
    sql = "SELECT * FROM addrbook"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    
    return render_template('appl.html', rows=result)

@app.route('/admin', methods=['POST', 'GET'])
def signup1():
    if request.method == 'POST':
        try:
            user_name1 = request.form.get('username')
            password1 = request.form.get('password')
            role1 = request.form.get('role')

            cursor = db_connection.cursor()
            sql = "INSERT INTO login (username, password, role) VALUES (%s, %s, %s)"
            cursor.execute(sql, (user_name1, password1, role1))
            db_connection.commit()
            cursor.close()
            
            return render_template('admin_page.html')
        
        except Exception as e:
            return f"An error occurred: {e}"

    return render_template('admin_page.html')

@app.route('/faculty', methods=['POST', 'GET'])
def faculty():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            roll_no = request.form.get('roll')
            dept = request.form.get('dept')
            sem = request.form.get('sem')
            year = request.form.get('year')

            # Insert data into the students table
            cursor = db_connection.cursor()
            sql_students = "INSERT INTO students (name, roll_no, dept, sem, year) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql_students, (name, roll_no, dept, sem, year))
            db_connection.commit()
            cursor.close()

            # Insert data into the class_1_chem table
            cursor = db_connection.cursor()
            sql_class_1_chem = "INSERT INTO class_1_chem (rollno, name) VALUES (%s, %s)"
            cursor.execute(sql_class_1_chem, (roll_no, name))
            db_connection.commit()
            cursor.close()

            return render_template('faculty.html')

        except mysql.connector.Error as err:
            print("MySQL Error:", err)
            return f"An error occurred: {err}"

    return render_template('faculty.html')


@app.route('/teacher', methods=['GET', 'POST'])
def teacher():
    if request.method == 'POST':
        # Add new assignment column
        assignment_name = request.form.get('assignment_name')
        if assignment_name:
            try:
                cursor = db_connection.cursor()
                add_column_query = f"ALTER TABLE class_1_chem ADD COLUMN {assignment_name} VARCHAR(100)"
                cursor.execute(add_column_query)
                db_connection.commit()
                cursor.close()
                print(f"Column '{assignment_name}' added successfully.")  # Debug statement
            except mysql.connector.Error as err:
                print("MySQL Error:", err)
        
        # Update assignment status
        column_name = request.form.get('column_name')
        roll_no = request.form.get('roll_no')
        if column_name and roll_no:
            try:
                cursor = db_connection.cursor()
                update_query = f"UPDATE class_1_chem SET {column_name} = 'yes' WHERE rollno = %s"
                cursor.execute(update_query, (roll_no,))
                db_connection.commit()
                cursor.close()
                print(f"Assignment for roll number {roll_no} updated to 'yes' in column '{column_name}'.")  # Debug statement
            except mysql.connector.Error as err:
                print("MySQL Error:", err)
                return f"An error occurred while updating assignment: {err}"
    return render_template('teacher.html')


if __name__ == "__main__":
    app.run(debug=True)



# @app.route('/add', methods = ['POST', 'GET'])
# def add():
#     return render_template("add.html")

# @app.route('/add1', methods = ['POST', 'GET'])
# def add1():
#     if request.method  == 'POST':
#         name = request.form['name']
#         watsapp_no = request.form['watsapp_no']
#         door_no = request.form['door_no']
#         street = request.form['street']
#         city = request.form['city']
#         pincode = request.form['pincode']
#         con=conn.connection.cursor()
#         sql = "insert into addrbook(name,watsapp_no,door_no,street,city,pincode) values  (%s,%s,%s,%s,%s,%s)"
#         result=con.execute(sql,(name,watsapp_no,door_no,street,city,pincode))
#         con.connection.commit()
#         con.close()
#         return  redirect(url_for('appl'))
        
#     return render_template('add.html')

# @app.route('/search',methods=['GET', 'POST'])
# def search():
    
#     if request.method  == 'POST':
#         uname = request.form['uname']
#         con=conn.connection.cursor()
#         con.execute('select * from addrbook where name like %s' ,{ '%' +uname + '%'})
#         result=con.fetchall()
#         return render_template('result.html',rows=result) 
    

#     return render_template('appl.html')

