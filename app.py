from flask import Flask,request,jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'library'

mysql = MySQL(app)

def getQuery(sql):
    cursor = mysql.connection.cursor()
    cursor.execute(sql)
    data=cursor.fetchall()
    return data

def Query(sql):
    cursor = mysql.connection.cursor()
    cursor.execute(sql)
    mysql.connection.commit()


@app.route("/")
def index():
    return {"code":200,"msg":"READY"}

@app.route("/get-books")
def getBooks():
    try:
        return {"code":200,"data":getQuery("select * from books")}
    except Exception as e:
        return {"code":400}

@app.route("/get-book/<book_id>")
def getBook(book_id):
    try:
        return {"code":200,"data":getQuery("select * from books where book_id={0}".format(book_id))}
    except Exception as e:
        return {"code":400}

@app.route("/new-book",methods=["POST"])
def addBook():
    try:
        name=request.form.get("name")
        Query("insert into books(name) values('{0}')".format(name))
        return {"code":200}
    except Exception as e:
        return {"code":400,"msg":str(e)}

@app.route("/update-book/<book_id>",methods=["PUT"])
def updateBook(book_id):
    try:
        name=request.form.get("name")
        Query("update books set name='{0}' where book_id={1}".format(name,book_id))
        return {"code":200}
    except Exception as e:
        return {"code":400}

@app.route("/delete-book/<book_id>",methods=["DELETE"])
def deleteBook(book_id):
    try:
        Query("delete from books where book_id={0}".format(book_id))
        return {"code":200}
    except Exception as e:
        return {"code":400}

if __name__ == '__main__':
    app.run(debug=True,use_reloader=True)
