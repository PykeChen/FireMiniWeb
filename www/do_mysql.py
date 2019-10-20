import mysql.connector
import re


def table_exists(con, table_name):  # 这个函数用来判断表是否存在
    sql = "show tables;"
    con.execute(sql)
    tables = [con.fetchall()]
    table_list = re.findall('(\'.*?\')', str(tables))
    table_list = [re.sub("'", '', each) for each in table_list]
    if table_name in table_list:
        return 1  # 存在返回1
    else:
        return 0


conn = mysql.connector.connect(user='root', password='password', database='test')
cursor = conn.cursor()

if not table_exists(cursor, 'user'):
    cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')

cursor.execute('insert into user (id, name) values (%s, %s)', ['2', 'Michael2'])
print('count', cursor.rowcount)

conn.commit()
cursor.close()

cursor = conn.cursor()
cursor.execute('select * from user where id = %s', ('1',))
print('values', cursor.fetchall())
cursor.close()
conn.close()
