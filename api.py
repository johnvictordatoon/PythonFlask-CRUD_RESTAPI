from flask import Flask, make_response, jsonify, request
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

def fetch_data(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data

@app.route("/")
def welcome():
    return """<h1>Vehicle Rental Database</h1>
    <p>Click <a href="http://127.0.0.1:5000/database">here</a> to proceed</p>
    <p><b><i>OR</i></b></p>
    <p>Search: [placeholder search box]</p>"""

@app.route("/database")
def the_database():
    data = fetch_data("""SELECT customers.CustomerID, customers.CustomerName, customers.ContactNumber,
    vehicles.VehicleID, vehicles.ManufacturerVehicle, vehicles.VehicleModel, vehicles.DailyRate, 
    rentals.RentalID, rentals.RentalStatus, rentals.StartDate, rentals.EndDate
    FROM customers
    JOIN rentals ON customers.CustomerID = rentals.CustomerID
    JOIN vehicles ON rentals.VehicleID = vehicles.VehicleID""")
    return make_response(jsonify(data), 200)

@app.route("/customers", methods=["GET"])
def get_customers():
    data = fetch_data("""SELECT * FROM customers""")
    return make_response(jsonify(data), 200)

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
    data = fetch_data("""SELECT ManufacturerVehicle, VehicleModel, DailyRate FROM Vehicles""")
    return make_response(jsonify(data), 200)

@app.route("/customers", methods=["POST"])
def add_customers():
    cur = mysql.connection.cursor()
    info = request.get_json()
    customername = info["CustomerName"]
    contactnumber = info["ContactNumber"]
    cur.execute("""INSERT INTO vehicle_rental.customers (CustomerName, ContactNumber) VALUES (%s, %s)""", (customername, contactnumber), )
    mysql.connection.commit()

    print("Affected Row(s): {}".format(cur.rowcount))
    affected_rows = cur.rowcount
    cur.close()

    return make_response(jsonify({"Message": "New Customer Added!", "Affected Rows": affected_rows}), 201)

@app.route("/vehicles", methods=["POST"])
def add_vehicles():
    cur = mysql.connection.cursor()
    info = request.get_json()
    manufacturervehicle = info["ManufacturerVehicle"]
    vehiclemodel = info["VehicleModel"]
    dailyrate = info["DailyRate"]
    cur.execute("""INSERT INTO vehicle_rental.vehicles (ManufacturerVehicle, VehicleModel, DailyRate) VALUES (%s, %s, %s)""", (manufacturervehicle, vehiclemodel, dailyrate), )
    mysql.connection.commit()

    print("Affected Row(s): {}".format(cur.rowcount))
    affected_rows = cur.rowcount
    cur.close()

    return make_response(jsonify({"Message": "New Vehicle Added!", "Affected Rows": affected_rows}), 201)

if __name__ == "__main__":
    app.run(debug=True)