from flask import *
import pypyodbc
from datetime import date

app=Flask(__name__)
app.secret_key = "a1b2c"
conn='Driver={SQL Server};Server=.;Database=sample;uid=sa;pwd=Admin@12345'


@app.route('/')
def index():
    return render_template('customer_login.html')

@app.route('/login',methods=["POST"])
def login():
    if request.method=="POST":
        cid=request.form["cid"]
        session['cus_id']=request.form["cid"]
        with pypyodbc.connect(conn) as con: 
            cur = con.cursor()
            cur.execute("select cid from customers where cid='%s'"%cid )
            customer_id=cur.fetchone()
            if customer_id:
                return redirect(url_for('home',msg=cid))
            else:
                error = "invalid customer id"
                return render_template('customer_login.html',msg=error)

@app.route('/home')
def home():
    if 'cus_id' in session:
        cid=session['cus_id']
        with pypyodbc.connect(conn) as con: 
            cur = con.cursor()
            cur.execute("select cname,ano,atype,balance from customers as c, account as a where c.cid=a.cid and c.cid='%s' group by cname,ano,atype,balance"%cid )
            rows=cur.fetchall()
        return render_template('customer_home.html',rows=rows)
    else:
        msg="session over, login again"
        return redirect(url_for('sessionover',msg=msg))

@app.route('/trans')
def trans():
    if 'cus_id' in session:
        return render_template('customer_trans.html')
    else:
        msg="session over, login again"
        return redirect(url_for('sessionover',msg=msg))

@app.route('/transconfirm',methods=["POST"])
def trans_confirm():
    if 'cus_id' in session:
        if request.method=="POST":
            cid=session['cus_id']
            amount=request.form["amount"]
            ttype=request.form['ttype']
            today=date.today()
            with pypyodbc.connect(conn) as con:
                cur = con.cursor()
                cur.execute("select ano,balance from account where cid='%s'"%cid)
                acc=cur.fetchone()                
                cur.execute("SELECT count(*) as date from trans where ano=? and CONVERT(DATE,tdate)=? and ttype=? group by CONVERT(DATE,tdate)",(acc[0],today,ttype))
                count=cur.fetchone()
                if ttype=='D':
                    if count and count[0]>=3:
                        error = "Error : Transaction limit exceed for deposit"
                        return render_template('customer_home.html',error=error)
                    elif int(amount)<=100000:
                        check_amount=int(acc[1])+int(amount)
                        cur.execute("insert into trans values(?,?,CURRENT_TIMESTAMP,?)",(acc[0],ttype,amount))
                        cur.execute("update account set balance=? where ano=?",(check_amount,acc[0]))
                    else:
                        error = "Error : Maximum 1,00,000 rupee can be Deposit per transaction, So transaction abort"
                        return render_template('customer_home.html',error=error)
                elif ttype=='W':
                    if count and count[0]>=3:
                        error = "Error : Transaction limit exceed for withdrawl"
                        return render_template('customer_home.html',error=error)
                    elif int(amount)<=10000:
                        if (int(acc[1])-int(amount))>=0 :
                            check_amount=int(acc[1])-int(amount)
                            cur.execute("insert into trans values(?,?,CURRENT_TIMESTAMP,?)",(acc[0],ttype,amount))
                            cur.execute("update account set balance=? where ano=?",(check_amount,acc[0]))
                        else:
                            error = "Error : insufficient balance, So transaction abort"
                            return render_template('customer_home.html',error=error) 
                    else:
                        error = "Error : Maximum 10,000 rupee can be widthdraw per transaction, So transaction abort"
                        return render_template('customer_home.html',error=error)   
                con.commit()
                return redirect(url_for('home'))
    else:
        msg="session over, login again"
        return redirect(url_for('sessionover',msg=msg))

@app.route('/logout')
def logout():
    session.pop('cus_id',None)
    return render_template('customer_login.html')

@app.route('/sessionover/<msg>')
def sessionover(msg):
    return render_template('customer_login.html',msg=msg)
    
            
if __name__=='__main__':
    app.run(debug='True')

