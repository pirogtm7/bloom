import mysql.connector
from client2 import Client2

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Qwerty12345',
    db='flower',
)

mycursor = mydb.cursor()


def connect(connection, id, name, lastname, area, street, entrance, apartment, floor):
    connection = mydb
    mycursor = connection.cursor()
    mycursor.execute("USE flower")
    sqlInsert = "INSERT INTO client (idclient, first_name, last_name, area, street,entrance,apartment,floor) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    customs = (id,name,lastname,area,street,entrance,apartment,floor)
    print(customs)
    mycursor.execute(sqlInsert,customs)
    mydb.commit()


def get_flower_low_price():
    list_of_low_price = []
    mycursor = mydb.cursor()
    sql = "SELECT product_id FROM oc_product WHERE price >=  500 AND price < 1000"
    mycursor.execute(sql)
    results = mycursor.fetchall()
    for i in range(len(results)):
        list_of_low_price.append(results[i][0])
    return list_of_low_price


def  get_flower_high_price():
    list_of_high_price = []
    mycursor = mydb.cursor()
    sql2 = "SELECT product_id FROM oc_product WHERE price >=  1000 AND price < 2000"
    mycursor.execute(sql2)
    results = mycursor.fetchall()
    for i in range(len(results)):
        list_of_high_price.append(results[i][0])
    return list_of_high_price


def get_results():
    mycursor = mydb.cursor()
    sql = "SELECT price From oc_product WHERE image = 'catalog/products/kazka.png"
    sql = "SELECT oc_product.product_id,oc_product.price,oc_product_description.description FROM oc_product_description INNER  JOIN oc_product  ON oc_product.product_id = oc_product_description.product_id LIMIT 0, 10000"
    mycursor.execute(sql)
    characteristiks = mycursor.fetchall()
    return characteristiks


def get_url_image(product_id):
    mycursor = mydb.cursor()
    sql = "SELECT url_image From oc_product WHERE product_id =" + str(product_id)
    mycursor.execute(sql)
    url = mycursor.fetchone()[0]
    return url


def get_price (product_id):
    mycursor = mydb.cursor()
    sql = "SELECT price From oc_product WHERE product_id =" + str(product_id)
    mycursor.execute(sql)
    price = mycursor.fetchone()
    return  price[0]


def get_description (product_id):
    mycursor = mydb.cursor()
    sql = "SELECT description FROM oc_product_description  WHERE oc_product_description.product_id =" + str(product_id)
    mycursor.execute(sql)
    description = mycursor.fetchone()
    return  description[0]
mycursor.close()
n = get_results()
##print("%s, %s, %s" % (row[0], row[1], row[2]))
#print(get_url_image(str(41)))
#print(get_flower_low_price())
#print(get_description(41) +"\n"+ str(get_price(41)))
