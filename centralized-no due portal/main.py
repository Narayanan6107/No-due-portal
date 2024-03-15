import MySQLdb
import mysql.connector
from flask import Flask,request, render_template,redirect,url_for,flash
from flask_mysqldb import MySQL


app=Flask(__name__)

app.config['MYSQL_HOST']= "localhost"
app.config['MYSQL_DB']= "flask"
app.config['MYSQL_USER']= "root"
app.config['MYSQL_PASSWORD']= "narayanan@123"
app.config['MYSQL_CURSORCLASS']="DictCursor"
app.secret_key="myapp"
conn = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    else:
        username = request.args.get('username')
        password = request.args.get('password')
        
    if username and password:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="narayanan@123",
            database="flask"
        )
        
        cursor = conn.cursor()
        
        sql = "SELECT role FROM login WHERE username = %s AND password = %s"
        cursor.execute(sql, (username, password))
        role = cursor.fetchone()
        
        conn.close()
        
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
            else:
                return "Unknown role"
        else:
            print("Invalid username or password")  # Debugging statement
            return "Invalid username or password"
    
    return render_template('login_trial.html')

@app.route('/appl/',methods=['GET', 'POST'])
def appl():
    
    con=conn.connection.cursor()
    sql="select * from  addrbook"
    con.execute(sql)
    result= con.fetchall()
    con.connection.commit()    
    return render_template('appl.html',rows=result)

@app.route('/admin', methods=['POST', 'GET'])
def signup1():
    if request.method == 'POST':
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="narayanan@123",
 
                database="flask"
            )

            user_name1 = request.form['username']
            password1 = request.form['password']
            role1 = request.form['role']

            cursor = conn.cursor()
            sql = "INSERT INTO login (username, password, role) VALUES (%s, %s, %s)"
            cursor.execute(sql, (user_name1, password1, role1))
            conn.commit()
            cursor.close()
            conn.close()
            
            return render_template('admin_page.html')
        
        except Exception as e:
            return f"An error occurred: {e}"

    return render_template('admin_page.html')

@app.route('/faculty', methods=['POST', 'GET'])
def faculty():
    if request.method == 'POST':
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="narayanan@123",
 
                database="flask"
            )

            name = request.form['name']
            roll_no = request.form['roll']
            dept = request.form['dept']
            sem = request.form['sem']
            year = request.form['year']

            cursor = conn.cursor()
            sql = "INSERT INTO login (roll_no, password, dept, sem, year) VALUES (%s, %s, %s,%s,%s)"
            cursor.execute(sql, (roll_no, name, dept, sem, year))
            conn.commit()
            cursor.close()
            conn.close()
            
            return render_template('faculty.html')
        
        except Exception as e:
            return f"An error occurred: {e}"

    return render_template('faculty.html')


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


if __name__ == "__main__":
    app.run(debug=True)