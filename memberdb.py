import pypyodbc
with pypyodbc.connect('Driver={SQL Server};Server=.;Database=FlaskDB;uid=sa;pwd=Admin@12345;') as conn:
    cur=conn.cursor()
    cur.execute("CREATE TABLE employee (empid int primary key, name varchar(255) not null, email varchar(255) not null, department varchar(255) not null, address varchar(255));")
    cur.execute("CREATE TABLE emp_login_credentials(empid int FOREIGN KEY REFERENCES employee(empid), password varchar(255))")
    cur.execute("CREATE TABLE posting (empid int FOREIGN KEY REFERENCES employee(empid), password varchar(255)) ")
    print("table created")
    conn.commit()
