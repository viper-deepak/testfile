import pypyodbc
with pypyodbc.connect('Driver={SQL Server};Server=.;Database=sample;uid=sa;pwd=Admin@12345;') as conn:
    cur=conn.cursor()
    cur.execute("create table customers(cid varchar(5) primary key,cname varchar(30));")
    cur.execute("create table account(ano varchar(10) primary key ,atype char check(atype in('S','C')),balance int default 0,cid varchar(5),foreign key(cid) references customers(cid));")
    cur.execute("create table trans(tid varchar(5) primary key,ano varchar(10) ,ttype char check(ttype in('D','W')),tdate timestamp ,tamount int,foreign key(ano) references account(ano));")
    cur.commit()