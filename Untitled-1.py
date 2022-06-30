                if count and count[0]>=3:
                    error = "Error : transaction limit exceed"
                    return render_template('customer_home.html',error=error)
                else:
                    if ttype=='D':
                        check_amount=int(acc[1])+int(amount)
                        cur.execute("insert into trans values(?,?,CURRENT_TIMESTAMP,?)",(acc[0],ttype,amount))
                        cur.execute("update account set balance=? where ano=?",(check_amount,acc[0]))
                    elif ttype=='W' and (int(acc[1])-int(amount))>=3000:
                        if int(amount)<=10000:
                            check_amount=int(acc[1])-int(amount)
                            cur.execute("insert into trans values(?,?,CURRENT_TIMESTAMP,?)",(acc[0],ttype,amount))
                            cur.execute("update account set balance=? where ano=?",(check_amount,acc[0]))
                        else:
                            error = "Error :Maximum 10,000 rupee can be widthdraw per transaction, So transaction abort"
                            return render_template('customer_home.html',error=error)   
                    else:
                        error = "Error : No Min Balance, So transaction abort"
                        return render_template('customer_home.html',error=error)