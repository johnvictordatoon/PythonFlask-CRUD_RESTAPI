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

def fetch_data(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data

@app.route("/vehicles", methods=["GET"])
def get_vehicles():
    data = fetch_data("""SELECT * FROM vehicles""")
    return make_response(jsonify(data), 200)


@app.route("/vehicles/<int:id>", methods=["GET"])
def get_vehicles_by_id(id):
    data = fetch_data("""SELECT * FROM vehicles WHERE VehicleID = {}""".format(id))
    return make_response(jsonify(data), 200)

@app.route("/vehicles/daily_rate", methods=["GET"])
def get_dailyrate_by_vehicles():
    data = fetch_data("""SELECT ManufacturerVehicle, VehicleType, DailyRate FROM Vehicles""")
    return make_response(jsonify(data), 200)

if __name__ == "__main__":
    app.run(debug=True)