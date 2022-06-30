from sqlite3 import connect
from flask import *
import pypyodbc
app=Flask(__name__)
app.secret_key = "a1b2c3"
conn='Driver={SQL Server};Server=.;Database=FlaskDB;uid=sa;pwd=Admin@12345'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin_index.html')


@app.route('/adminlogin',methods=["POST"])
def adminlogin():
    name=request.form["uname"]
    password=request.form["password"]
    if password=="admin":
        return redirect(url_for('admin_home'))

@app.route('/adminhome')
def admin_home():
    return render_template('admin_home.html')

@app.route('/add')
def add():
    return render_template('add_emp.html')

@app.route('/save',methods=["POST","GET"])
def save_details():
    if request.method=="POST":
        userid = request.form["emp_id"]  
        name = request.form["name"]  
        email = request.form["mail"]  
        dept = request.form["dept"]  
        address = request.form["address"]  
        with pypyodbc.connect(conn) as con: 
            cur = con.cursor()  
            cur.execute("INSERT into Employee (empid,name, email, department, address) values (?,?,?,?,?)",(userid,name,email,dept,address))  
            con.commit()   
        return render_template('emp_details_added.html')



@app.route('/view')
def view():
    con= pypyodbc.connect(conn)
    cur=con.cursor()
    cur.execute("select * from employee")
    rows=cur.fetchall()
    return render_template('view_emp.html',rows=rows)

@app.route('/update')
def update():
    return render_template('update_emp.html')

@app.route('/empupdate',methods=["POST"])
def empupdate():
    if request.method=="POST":
        userid = request.form["emp_id"]  
        name = request.form["name"]  
        email = request.form["mail"]  
        dept = request.form["dept"]  
        address = request.form["address"]  
        with pypyodbc.connect(conn) as con: 
            cur = con.cursor()  
            cur.execute("UPDATE Employee set  name=?, email=?, department=?, address=? where empid=?",(name,email,dept,address,userid))  
            con.commit()   
        return render_template('emp_details_update.html')


@app.route('/delete')
def delete():
    return render_template('delete_emp.html')

@app.route('/empdelete',methods=["POST"])
def empdelete():
    if request.method=="POST":
        empid = request.form["emp_id"]   
        with pypyodbc.connect(conn) as con: 
            cur = con.cursor()  
            cur.execute("Delete from Employee where empid=%s"%empid)  
            con.commit()     
        return render_template('emp_details_delete.html')

@app.route('/employ')
def employ():
    return render_template('employee_index.html')

@app.route('/emphome/<empid>')
def emphome(empid):
    with pypyodbc.connect(conn) as con:
        cur=con.cursor()
        cur.execute("select e.empid,name,email,designation, department, address from employee as e, posting as d where e.empid=d.empid and e.empid=%s group by e.empid,name,email,d.designation,department,address"%empid)
        rows=cur.fetchall()
    return render_template('emp_profile.html',rows=rows)

@app.route('/login',methods=["POST"])
def emplogin():
    if request.method=='POST':
        empid=request.form["empid"]
        password=request.form["password"]
        with pypyodbc.connect(conn) as con: 
            cur = con.cursor() 
            cur.execute("select password from emp_login_credentials where empid=%s"%empid)
            passkey=cur.fetchone()
            if passkey[0]==password:
                session['emloyid']= empid
                return redirect(url_for('emphome',empid=empid))
            else:
                error = "invalid password"
                return render_template('employee_index.html',error=error)  
    else:
        return "error"

@app.route('/empregister')
def register():
    return render_template('emp_register.html')

@app.route('/signup',methods=["POST"])
def sign_up():
    if request.method=='POST':
        empid=request.form["empid"]
        password=request.form["password"]
        cpassword=request.form["cpassword"]
        if password==cpassword:
            with pypyodbc.connect(conn) as con: 
                cur = con.cursor() 
                cur.execute("select empid from employee where empid=%s"%empid)
                id=cur.fetchone()
                if id and id[0]==int(empid):
                    cur.execute("select empid from emp_login_credentials where empid=%s"%empid)
                    employid=cur.fetchone()
                    if employid:
                        error = "already had a account,pls login"
                        return render_template('emp_register.html',error=error)
                    else:
                        cur.execute("insert into emp_login_credentials(empid, password) values(?,?)",(empid,password))
                        cur.commit()
                        return redirect(url_for('employ'))  
                else:
                    error = "invalid employee id"
                    return render_template('emp_register.html',error=error)  
        else:
             error = "both password should be same"  
             return render_template('emp_register.html',error=error)  

@app.route('/emplogout')
def emp_logout():
    return redirect(url_for('employ'))
             
@app.route('/changepassword')     
def changepassword():
    return render_template('change_password.html')

@app.route('/password',methods=["POST"])
def password():
    if request.method=="POST":
        empid=request.form["empid"]
        oldpass=request.form["oldpassword"]
        newpass=request.form["newpassword"]
        confirmpass=request.form["cpassword"]
        if newpass==confirmpass:
            with pypyodbc.connect(conn) as con: 
                cur = con.cursor()  
                cur.execute("select password from emp_login_credentials where empid=%s"%empid)
                passkey=cur.fetchone()
                if passkey[0]==oldpass:
                    cur.execute("update emp_login_credentials set password=? where empid=?",(newpass,empid)) 
                    con.commit()  
                    return redirect(url_for('emphome',empid=empid))
                else:
                    error = "enter correct old password"  
                    return render_template('change_password.html',error=error) 
        else:
                error = "both password should be same"  
                return render_template('change_password.html',error=error) 

if __name__=='__main__':
    app.run(debug=True)
