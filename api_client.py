from flask import Flask, make_response, jsonify, request, render_template_string
from flask_mysqldb import MySQL
import jwt
from functools import wraps

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "admin5678"
app.config["MYSQL_DB"] = "vehicle_rental"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config['SECRET_KEY'] = 'KEYSECRET'

mysql = MySQL(app)

# JWT Token Required Decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({'message': 'Token is invalid'}), 401

        return f(*args, **kwargs)

    return decorated

# Example JWT Token Generation
@app.route('/login', methods=['GET'])
def login():
    auth = request.authorization
    if auth and auth.password == 'password':
        token = jwt.encode({'user': auth.username}, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'token': token})

    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

@app.route('/protected')
@token_required
def protected():
    return jsonify({'message': 'This is a protected endpoint'})

def fetch_data(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data

@app.route("/")
@token_required
def welcome():
    return """<h1>Vehicle Rental Database</h1>
    <p><a href="search">Search</a> through the database</p>
    <p><a href="http://127.0.0.1:5000/database">View</a> entire database</p>
    <p><a href="http://127.0.0.1:5000/addcustomer">Add</a> a customer</p>
    <p><a href="http://127.0.0.1:5000/addvehicle">Add</a> a vehicle</p>
    <p><a href="http://127.0.0.1:5000/addrental">Add</a> a rental information (related to the customer)</p>
    <p><a href="http://127.0.0.1:5000/updatecustomer">Edit</a> a customer</p>
    <p><a href="http://127.0.0.1:5000/updatevehicle">Edit</a> a vehicle</p>
    <p><a href="http://127.0.0.1:5000/updaterental">Edit</a> a rental information (related to the customer)</p>
    <p><a href="http://127.0.0.1:5000/deleterental">Delete</a> rental (do this <b>first</b> before deleting others)</p>
    """

# get entire database
@app.route("/database")
@token_required
def the_database():
    data = fetch_data("""SELECT customers.CustomerName, customers.ContactNumber, vehicles.ManufacturerVehicle, vehicles.VehicleModel, rentals.RentalStatus, rentals.StartDate, rentals.EndDate
    FROM Customers
    JOIN rentals ON customers.CustomerID = rentals.CustomerID
    JOIN vehicles ON rentals.VehicleID = vehicles.VehicleID""")
    return make_response(jsonify(data), 200)

# get customers
@app.route("/customers", methods=["GET"])
@token_required
def get_customers_client():
    data = fetch_data("""SELECT * FROM customers""")
    return make_response(jsonify(data), 200)

# get customers by id
@app.route("/customers/<int:id>", methods=["GET"])
@token_required
def get_customers_by_id_client(id):
    data = fetch_data("""SELECT * FROM customers WHERE CustomerID = {}""".format(id))
    return make_response(jsonify(data), 200)

# get vehicles
@app.route("/vehicles", methods=["GET"])
@token_required
def get_vehicles_client():
    data = fetch_data("""SELECT * FROM vehicles""")
    return make_response(jsonify(data), 200)

# get vehicles by id
@app.route("/vehicles/<int:id>", methods=["GET"])
@token_required
def get_vehicles_by_id_client(id):
    data = fetch_data("""SELECT * FROM vehicles WHERE VehicleID = {}""".format(id))
    return make_response(jsonify(data), 200)

# get daily rate by vehicles
@app.route("/vehicles/daily_rate", methods=["GET"])
@token_required
def get_dailyrate_by_vehicles_client():
    data = fetch_data("""SELECT ManufacturerVehicle, VehicleModel, DailyRate FROM Vehicles""")
    return make_response(jsonify(data), 200)

# get rentals
@app.route("/rentals", methods=["GET"])
def get_rentals_client():
    data = fetch_data("""SELECT * FROM rentals""")
    return make_response(jsonify(data), 200)

# get rentals by id
@app.route("/rentals/<int:id>", methods=["GET"])
@token_required
def get_rentals_by_id_client(id):
    data = fetch_data("""SELECT * FROM rentals WHERE RentalID = {}""".format(id))
    return make_response(jsonify(data), 200)

# add customers
@app.route("/customers", methods=["POST"])
@token_required
def add_customers_client():
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

# add vehicles
@app.route("/vehicles", methods=["POST"])
@token_required
def add_vehicles_client():
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

# add rental
@app.route("/rentals", methods=["POST"])
@token_required
def add_rental_client():
    cur = mysql.connection.cursor()
    info = request.get_json()
    customerid = info["CustomerID"]
    vehicleid = info["VehicleID"]
    rentalstatus = info["RentalStatus"]
    startdate = info["StartDate"]
    enddate = info["End Date"]
    cur.execute("""INSERT INTO vehicle_rental.rentals (CustomerID, VehicleID, RentalStatus, StartDate, EndDate) VALUES (%s, %s, %s, %s, %s)""", (customerid, vehicleid, rentalstatus, startdate, enddate), )
    mysql.connection.commit()

    print("Affected Row(s): {}".format(cur.rowcount))
    affected_rows = cur.rowcount
    cur.close()

    return make_response(jsonify({"Message": "Rental Added!", "Affected Rows": affected_rows}), 200)


@app.route("/customers/<int:id>", methods=["PUT"])
@token_required
def update_customers_client(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    customername = info["CustomerName"]
    contactnumber = info["ContactNumber"]
    cur.execute("""UPDATE vehicle_rental.customers SET CustomerName = %s, ContactNumber = %s WHERE (CustomerID = %s);""", (customername, contactnumber, id), )
    mysql.connection.commit()

    print("Affected Row(s): {}".format(cur.rowcount))
    affected_rows = cur.rowcount
    cur.close()

    return make_response(jsonify({"Message": "Customer Updated!", "Affected Rows": affected_rows}), 201)

@app.route("/vehicles/<int:id>", methods=["PUT"])
@token_required
def update_vehicles_client(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    manufacturervehicle = info["ManufacturerVehicle"]
    vehiclemodel = info["VehicleModel"]
    dailyrate = info["DailyRate"]
    cur.execute("""UPDATE vehicle_rental.vehicles SET ManufacturerVehicle = %s, VehicleModel = %s, DailyRate = %s WHERE (VehicleID = %s)""", (manufacturervehicle, vehiclemodel, dailyrate, id), )
    mysql.connection.commit()

    print("Affected Row(s): {}".format(cur.rowcount))
    affected_rows = cur.rowcount
    cur.close()

    return make_response(jsonify({"Message": "Vehicle Updated!", "Affected Rows": affected_rows}), 200)

@app.route("/rentals/<int:id>", methods=["PUT"])
@token_required
def update_rental_client(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    customerid = info["CustomerID"]
    vehicleid = info["VehicleID"]
    rentalstatus = info["RentalStatus"]
    startdate = info["StartDate"]
    enddate = info["End Date"]
    cur.execute("""UPDATE vehicle_rental.rentals SET CustomerID = %s, VehicleID = %s, RentalStatus = %s, StartDate = %s, EndDate = %s WHERE (RentalID = %s)""", (customerid, vehicleid, rentalstatus, startdate, enddate, id), )
    mysql.connection.commit()

    print("Affected Row(s): {}".format(cur.rowcount))
    affected_rows = cur.rowcount
    cur.close()

    return make_response(jsonify({"Message": "Rental Updated!", "Affected Rows": affected_rows}), 200)

# delete the vehicle by id
@app.route("/customers/<int:id>", methods=["DELETE"])
@token_required
def delete_customer_client(id):
    cur = mysql.connection.cursor()
    cur.execute("""DELETE FROM vehicle_rental.customers WHERE (CustomerID = %s);""", (id, ))
    mysql.connection.commit()
    affected_rows = cur.rowcount
    cur.close()
    return make_response(jsonify({"Message": "Customer Deleted!", "Affected Rows": affected_rows}), 200)

# delete the vehicle by id
@app.route("/vehicles/<int:id>", methods=["DELETE"])
@token_required
def delete_vehicle_client(id):
    cur = mysql.connection.cursor()
    cur.execute("""DELETE FROM vehicle_rental.vehicles WHERE (VehicleID = %s);""", (id, ))
    mysql.connection.commit()
    affected_rows = cur.rowcount
    cur.close()
    return make_response(jsonify({"Message": "Vehicle Deleted!", "Affected Rows": affected_rows}), 200)

# delete the rental by id
@app.route("/rentals/<int:id>", methods=["DELETE"])
@token_required
def delete_rental_client(id):
    cur = mysql.connection.cursor()
    cur.execute("""DELETE FROM vehicle_rental.rentals WHERE (RentalID = %s);""", (id, ))
    mysql.connection.commit()
    affected_rows = cur.rowcount
    cur.close()
    return make_response(jsonify({"Message": "Rental Deleted!", "Affected Rows": affected_rows}), 200)

# run the program
if __name__ == "__main__":
    app.run(debug=True)