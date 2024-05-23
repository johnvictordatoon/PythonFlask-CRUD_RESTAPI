from flask import Flask, make_response, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# Required
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "admin5678"
app.config["MYSQL_DB"] = "vehicle_rental"

# Extra configs, optional:
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route("/")
def helloworld():
    return "<p>Hello World</p>"

@app.route("/vehicles", methods=["GET"])
def get_vehicles():
    cur = mysql.connection.cursor()
    query = """
    SELECT * FROM vehicles
    """
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return make_response(jsonify(data), 200)

if __name__ == "__main__":
    app.run(debug=True)