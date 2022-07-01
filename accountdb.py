import pypyodbc
with pypyodbc.connect('Driver={SQL Server};Server=.;Database=sample;uid=sa;pwd=Admin@12345;') as conn:
    cur=conn.cursor()
    cur.execute("create table customers(cid varchar(5) primary key,cname varchar(30));")
    cur.execute("create table account(ano varchar(10) primary key ,atype char check(atype in('S','C')),balance int default 0,cid varchar(5),foreign key(cid) references customers(cid));")
    cur.execute("create table trans(tid varchar(20) primary key  NOT NULL,ano varchar(10) ,ttype char(6) check(ttype in('Debit','Credit')),tdate DATETIME NOT NULL ,tamount int,foreign key(ano) references account(ano));")
    cur.execute("create table trans_history(tid varchar(20) NOT NULL primary key,ano varchar(10) foreign key references account(ano),ttype char(6) check(ttype in('Debit','Credit')),tdate DATETIME NOT NULL ,tamount int, status varchar(20) , updated_balance int);")
    cur.commit()