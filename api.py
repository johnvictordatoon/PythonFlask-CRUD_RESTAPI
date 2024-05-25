from flask import Flask, make_response, jsonify, request, render_template_string
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "admin5678"
app.config["MYSQL_DB"] = "vehicle_rental"

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
    <p><a href="http://127.0.0.1:5000/database">View</a> entire database</p>
    <p><a href="http://127.0.0.1:5000/add_customer">Add</a> customer</p>
    <p><a href="http://127.0.0.1:5000/add_vehicle">Add Vehicle</a></p>
    <p><a href="edit">Edit</a> an entry</p>
    <p><a href="delete">Delete</a> an entry</p>
    <p><a href="search">Search</a> through the database</p>
    <p><b><i>OR</i></b></p>
    <p>Search: [placeholder search box]</p>"""

# get entire database
@app.route("/database")
def the_database():
    data = fetch_data("""SELECT customers.CustomerID, customers.CustomerName, customers.ContactNumber,
    vehicles.VehicleID, vehicles.ManufacturerVehicle, vehicles.VehicleModel, vehicles.DailyRate, 
    rentals.RentalID, rentals.RentalStatus, rentals.StartDate, rentals.EndDate
    FROM customers
    JOIN rentals ON customers.CustomerID = rentals.CustomerID
    JOIN vehicles ON rentals.VehicleID = vehicles.VehicleID""")
    return make_response(jsonify(data), 200)

# get customers
@app.route("/customers", methods=["GET"])
def get_customers():
    data = fetch_data("""SELECT * FROM customers""")
    return make_response(jsonify(data), 200)

# get vehicles
@app.route("/vehicles", methods=["GET"])
def get_vehicles():
    data = fetch_data("""SELECT * FROM vehicles""")
    return make_response(jsonify(data), 200)

# get vehicles by id
@app.route("/vehicles/<int:id>", methods=["GET"])
def get_vehicles_by_id(id):
    data = fetch_data("""SELECT * FROM vehicles WHERE VehicleID = {}""".format(id))
    return make_response(jsonify(data), 200)

# get daily rate by vehicles
@app.route("/vehicles/daily_rate", methods=["GET"])
def get_dailyrate_by_vehicles():
    data = fetch_data("""SELECT ManufacturerVehicle, VehicleModel, DailyRate FROM Vehicles""")
    return make_response(jsonify(data), 200)

# get rentals
@app.route("/rentals", methods=["GET"])
def get_rentals():
    data = fetch_data("""SELECT * FROM rentals""")
    return make_response(jsonify(data), 200)

# add a customer
@app.route("/addcustomer", methods=["GET", "POST"])
def add_customer():
    if request.method == "POST":
        customername = request.form["CustomerName"]
        contactnumber = request.form["ContactNumber"]
        affected_rows = add_customer_to_db(customername, contactnumber)
        return make_response(jsonify({"Message": "New Customer Added!", "Affected Rows": affected_rows}), 201)
    return render_template_string("""
    <h1>Add a Customer</h1>
    <form method="post">
        Customer Name: <input type="text" name="CustomerName"><br>
        Contact Number: <input type="text" name="ContactNumber"><br>
        <button type="submit">Add</button>
    </form>
    """)
# add the customer to the db
def add_customer_to_db(customername, contactnumber):
    cur = mysql.connection.cursor()
    cur.execute("""INSERT INTO vehicle_rental.customers (CustomerName, ContactNumber) VALUES (%s, %s)""", (customername, contactnumber))
    mysql.connection.commit()
    affected_rows = cur.rowcount
    cur.close()
    return affected_rows

# add a vehicle
@app.route("/addvehicle", methods=["GET", "POST"])
def add_vehicle():
    if request.method == "POST":
        manufacturervehicle = request.form["ManufacturerVehicle"]
        vehiclemodel = request.form["VehicleModel"]
        dailyrate = request.form["DailyRate"]
        affected_rows = add_vehicle_to_db(manufacturervehicle, vehiclemodel, dailyrate)
        return make_response(jsonify({"Message": "New Vehicle Added!", "Affected Rows": affected_rows}), 201)
    return render_template_string("""
    <h1>Add a Vehicle</h1>
    <form method="post">
        Manufacturer: <input type="text" name="ManufacturerVehicle"><br>
        Model: <input type="text" name="VehicleModel"><br>
        Daily Rate: <input type="text" name="DailyRate"><br>
        <button type="submit">Add</button>
    </form>
    """)

# add the vehicle to the db
def add_vehicle_to_db(manufacturervehicle, vehiclemodel, dailyrate):
    cur = mysql.connection.cursor()
    cur.execute("""INSERT INTO vehicle_rental.vehicles (ManufacturerVehicle, VehicleModel, DailyRate) VALUES (%s, %s, %s)""", (manufacturervehicle, vehiclemodel, dailyrate))
    mysql.connection.commit()
    affected_rows = cur.rowcount
    cur.close()
    return affected_rows

# edit the customer by id
@app.route("/customers/<int:id>", methods=["PUT"])
def update_customers(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    customername = info["CustomerName"]
    contactnumber = info["ContactNumber"]
    cur.execute("""UPDATE vehicle_rental.customers SET CustomerName = %s, ContactNumber = %s WHERE (CustomerID = %s);""", (customername, contactnumber, id))
    mysql.connection.commit()
    affected_rows = cur.rowcount
    cur.close()
    return make_response(jsonify({"Message": "Customer Updated!", "Affected Rows": affected_rows}), 201)

# edit the vehicle by id
@app.route("/vehicles/<int:id>", methods=["PUT"])
def update_vehicles(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    manufacturervehicle = info["ManufacturerVehicle"]
    vehiclemodel = info["VehicleModel"]
    dailyrate = info["DailyRate"]
    cur.execute("""UPDATE vehicle_rental.vehicles SET ManufacturerVehicle = %s, VehicleModel = %s, DailyRate = %s WHERE (VehicleID = %s)""", (manufacturervehicle, vehiclemodel, dailyrate, id))
    mysql.connection.commit()
    affected_rows = cur.rowcount
    cur.close()
    return make_response(jsonify({"Message": "Vehicle Updated!", "Affected Rows": affected_rows}), 200)

# delete the customer by id
@app.route("/customers/<int:id>", methods=["DELETE"])
def delete_customers(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    cur.execute("""DELETE FROM vehicle_rental.customers WHERE (CustomerID = %s);""", (id,))
    mysql.connection.commit()
    affected_rows = cur.rowcount
    cur.close()
    return make_response(jsonify({"Message": "Customer Deleted!", "Affected Rows": affected_rows}), 200)

# delete the customer by id
@app.route("/vehicles/<int:id>", methods=["DELETE"])
def delete_vehicles(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    cur.execute("""DELETE FROM vehicle_rental.vehicles WHERE (VehicleID = %s);""", (id,))
    mysql.connection.commit()
    affected_rows = cur.rowcount
    cur.close()
    return make_response(jsonify({"Message": "Vehicle Deleted!", "Affected Rows": affected_rows}), 200)

# run the program
if __name__ == "__main__":
    app.run(debug=True)