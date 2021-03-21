import pymysql

def insertData():

    db = pymysql.connect(host="mysql.FullHouse.secoder.local",port=3306,user="root",passwd="kuaishou",db="kuaishou",charset='utf8')

    #使用cursor()方法创建一个游标对象 cursor
    cursor = db.cursor()

    #使用execute()方法执行sql查询
    cursor.execute("insert into user(id) values(3)")

    db.commit()

    db.close()
