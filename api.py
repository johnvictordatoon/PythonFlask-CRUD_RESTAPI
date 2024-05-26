from flask import Flask, make_response, jsonify, request, render_template_string, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "admin5678"
app.config["MYSQL_DB"] = "vehicle_rental"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

# main menu
@app.route("/mainmenu", methods=["GET"])
def mainmenu():
    return render_template_string("""
    <h1>Vehicle Rental Database</h1>
    <p><a href="http://127.0.0.1:5000/search">Search</a> through the database</p>
    <p><a href="http://127.0.0.1:5000/database">View</a> entire database</p>
    <p><a href="http://127.0.0.1:5000/addcustomer">Add</a> a customer</p>
    <p><a href="http://127.0.0.1:5000/addvehicle">Add</a> a vehicle</p>
    <p><a href="http://127.0.0.1:5000/addrental">Add</a> a rental information (related to the customer)</p>
    <p><a href="http://127.0.0.1:5000/updatecustomer">Edit</a> a customer</p>
    <p><a href="http://127.0.0.1:5000/updatevehicle">Edit</a> a vehicle</p>
    <p><a href="http://127.0.0.1:5000/updaterental">Edit</a> a rental information (related to the customer)</p>
    <p><a href="http://127.0.0.1:5000/deleterental">Delete</a> rental</p>
    <p><a href="http://127.0.0.1:5000/deletecustomer">Delete</a> customer (must delete <b>first</b> the rental data)</p>
    <p><a href="http://127.0.0.1:5000/deletevehicle">Delete</a> vehicle (must delete <b>first</b> the rental data)</p>
    """)

# fetch get queries
def fetch_data(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data

# get entire database
@app.route("/database", methods=["GET"])
def the_database():
    data = fetch_data("""SELECT customers.CustomerName, customers.ContactNumber, vehicles.ManufacturerVehicle, vehicles.VehicleModel, rentals.RentalStatus, rentals.StartDate, rentals.EndDate
    FROM Customers
    JOIN rentals ON customers.CustomerID = rentals.CustomerID
    JOIN vehicles ON rentals.VehicleID = vehicles.VehicleID""")
    return make_response(jsonify(data), 200)

# add a customer
@app.route("/addcustomer", methods=["GET", "POST"])
def add_customer():
    if request.method == "POST":
        customername = request.form["CustomerName"]
        contactnumber = request.form["ContactNumber"]
        affected_rows = add_customer_to_db(customername, contactnumber)
        if affected_rows > 0:
            return render_template_string("""
            <h1>Customer Added!</h1>
            <p><a href="/mainmenu">Main Menu</a></p>
            """)
        else:
            return render_template_string("""
            <h1>Failed to Add Customer</h1>
            <p><a href="/addcustomer">Go Back</a></p>
            """)
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

# add a rental
@app.route("/addrental", methods=["GET", "POST"])
def add_rental():
    if request.method == "POST":
        customerid = request.form["CustomerID"]
        vehicleid = request.form["VehicleID"]
        rentalstatus = request.form["RentalStatus"]
        startdate = request.form["StartDate"]
        enddate = request.form["EndDate"]
        affected_rows = add_rental_to_db(customerid, vehicleid, rentalstatus, startdate, enddate)
        if affected_rows > 0:
            return render_template_string("""
            <h1>Rental Added!</h1>
            <p><a href="/mainmenu">Main Menu</a></p>
            """)
        else:
            return render_template_string("""
            <h1>Failed to Add Rental</h1>
            <p><a href="/addrental">Go Back</a></p>
            """)
    return render_template_string("""
    <h1>Add a Rental</h1>
    <form method="post">
        Customer ID: <input type="text" name="CustomerID"><br>
        Vehicle ID: <input type="text" name="VehicleID"><br>
        Rental Status: <input type="text" name="RentalStatus"><br>
        Start Date: <input type="text" name="StartDate"><br>
        End Date: <input type="text" name="EndDate"><br>
        <button type="submit">Add</button>
    </form>
    """)

# add the rental to the db
def add_rental_to_db(customerid, vehicleid, rentalstatus, startdate, enddate):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM customers WHERE CustomerID = %s", (customerid,))
    if not cur.fetchone():
        return 0
    
    cur.execute("SELECT * FROM vehicles WHERE VehicleID = %s", (vehicleid,))
    if not cur.fetchone():
        return 0
    
    cur.execute("""INSERT INTO vehicle_rental.rentals (CustomerID, VehicleID, RentalStatus, StartDate, EndDate) VALUES (%s, %s, %s, %s, %s)""", (customerid, vehicleid, rentalstatus, startdate, enddate))
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
        if affected_rows > 0:
            return render_template_string("""
            <h1>Vehicle Added!</h1>
            <p><a href="/mainmenu">Main Menu</a></p>
            """)
        else:
            return render_template_string("""
            <h1>Failed to Add Vehicle</h1>
            <p><a href="/addvehicle">Go Back</a></p>
            """)
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

# edit the customer
# PUT not working :(
@app.route("/updatecustomer", methods=["GET", "POST"])
def update_customer():
    if request.method == "POST":
        customerid = request.form["CustomerID"]
        customername = request.form["CustomerName"]
        contactnumber = request.form["ContactNumber"]
        affected_rows = update_customer_in_db(customerid, customername, contactnumber)
        if affected_rows > 0:
            return render_template_string("""
            <h1>Customer Updated!</h1>
            <p><a href="/mainmenu">Main Menu</a></p>
            """)
        else:
            return render_template_string("""
            <h1>Failed to Update Customer</h1>
            <p><a href="/updatecustomer">Go Back</a></p>
            """)
    return render_template_string("""
    <h1>Update Customer</h1>
    <form method="post" action="/updatecustomer?_method=PUT">
        Customer ID: <input type="text" name="CustomerID"><br>
        Customer Name: <input type="text" name="CustomerName"><br>
        Contact Number: <input type="text" name="ContactNumber"><br>
        <button type="submit">Update</button>
    </form>
    """)

def update_customer_in_db(customerid, customername, contactnumber):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE vehicle_rental.customers SET CustomerName = %s, ContactNumber = %s WHERE CustomerID = %s", (customername, contactnumber, customerid))
    mysql.connection.commit()
    affected_rows = cur.rowcount
    cur.close()
    return affected_rows

# edit the vehicle
# PUT not working :(
@app.route("/updatevehicle", methods=["GET", "POST"])
def update_vehicle():
    if request.method == "POST":
        vehicleid = request.form["VehicleID"]
        manufacturervehicle = request.form["ManufacturerVehicle"]
        vehiclemodel = request.form["VehicleModel"]
        dailyrate = request.form["DailyRate"]
        affected_rows = update_vehicle_in_db(vehicleid, manufacturervehicle, vehiclemodel, dailyrate)
        if affected_rows > 0:
            return render_template_string("""
            <h1>Vehicle Updated!</h1>
            <p><a href="/mainmenu">Main Menu</a></p>
            """)
        else:
            return render_template_string("""
            <h1>Failed to Update Vehicle</h1>
            <p><a href="/updatevehicle">Go Back</a></p>
            """)
    return render_template_string("""
    <h1>Update Vehicle</h1>
    <form method="post" action="/updatevehicle?_method=PUT">
        Vehicle ID: <input type="text" name="VehicleID"><br>
        Manufacturer: <input type="text" name="ManufacturerVehicle"><br>
        Model: <input type="text" name="VehicleModel"><br>
        Daily Rate: <input type="text" name="DailyRate"><br>
        <button type="submit">Update</button>
    </form>
    """)

def update_vehicle_in_db(vehicleid, manufacturervehicle, vehiclemodel, dailyrate):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE vehicle_rental.vehicles SET ManufacturerVehicle = %s, VehicleModel = %s, DailyRate = %s WHERE VehicleID = %s", (manufacturervehicle, vehiclemodel, dailyrate, vehicleid))
    mysql.connection.commit()
    affected_rows = cur.rowcount
    cur.close()
    return affected_rows

# edit the rental
# PUT not working :(
@app.route("/updaterental", methods=["GET", "POST"])
def update_rental():
    if request.method == "POST":
        rentalid = request.form["RentalID"]
        rentalstatus = request.form["RentalStatus"]
        startdate = request.form["StartDate"]
        enddate = request.form["EndDate"]
        affected_rows = update_rental_in_db(rentalid, rentalstatus, startdate, enddate)
        if affected_rows > 0:
            return render_template_string("""
            <h1>Rental Updated!</h1>
            <p><a href="/mainmenu">Main Menu</a></p>
            """)
        else:
            return render_template_string("""
            <h1>Failed to Update Rental</h1>
            <p><a href="/updaterental">Go Back</a></p>
            """)
    return render_template_string("""
    <h1>Update Rental</h1>
    <form method="post" action="/updaterental?_method=PUT">
        Rental ID: <input type="text" name="RentalID"><br>
        Rental Status: <input type="text" name="RentalStatus"><br>
        Start Date: <input type="text" name="StartDate"><br>
        End Date: <input type="text" name="EndDate"><br>
        <button type="submit">Update</button>
    </form>
    """)

def update_rental_in_db(rentalid, rentalstatus, startdate, enddate):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE vehicle_rental.rentals SET RentalStatus = %s, StartDate = %s, EndDate = %s WHERE RentalID = %s", (rentalstatus, startdate, enddate, rentalid))
    mysql.connection.commit()
    affected_rows = cur.rowcount
    cur.close()
    return affected_rows

# delete rental
# DELETE not working :(
@app.route("/deleterental", methods=["GET", "POST"])
def delete_rental():
    if request.method == "POST":
        rentalid = request.form["RentalID"]
        if rentalid:
            rentals_deleted = delete_rental_in_db(rentalid)
            if rentals_deleted > 0:
                return render_template_string("""
                <b><p>Rental Data Deleted.</p></b>
                <p><a href="/mainmenu">Main Menu</a></p>
                """)
            else:
                return render_template_string("""
                <b><p>ID doesn't exist.</p></b>
                <p><a href="/deleterental">Go Back</a></p>
                """)
    return render_template_string("""
    <h1>Delete Data</h1>
    <p>Note: All data related to the ID will be deleted.</p>
    <form method="post" action="/deleterental?_method=DELETE">
        Find ID: <input type="text" name="RentalID"><br>
        <button type="submit">Delete</button>
    </form>
    """)

def delete_rental_in_db(rentalid):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM vehicle_rental.rentals WHERE RentalID = %s", (rentalid,))
    rentals_deleted = cur.rowcount
    mysql.connection.commit()
    cur.close()
    return rentals_deleted

# delete customer
# DELETE not working :(
@app.route("/deletecustomer", methods=["GET", "POST"])
def delete_customer():
    if request.method == "POST":
        customerid = request.form["CustomerID"]
        if customerid:
            customers_deleted = delete_customer_in_db(customerid)
            if customers_deleted > 0:
                return render_template_string("""
                <b><p>Customer Data Deleted.</p></b>
                <p><a href="/mainmenu">Main Menu</a></p>
                """)
            else:
                return render_template_string("""
                <b><p>ID doesn't exist.</p></b>
                <p><a href="/deletecustomer">Go Back</a></p>
                """)
    return render_template_string("""
    <h1>Delete Customer</h1>
    <p><b>IMPORTANT</b>: Must delete the <b>rental</b> data associated by the deleted ID first. Otherwise, error will occur.</p>
    <form method="post" action="/deletecustomer?_method=DELETE">
        Find ID (Customer): <input type="text" name="CustomerID"><br>
        <button type="submit">Delete</button>
    </form>
    """)

def delete_customer_in_db(customerid):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM vehicle_rental.customers WHERE CustomerID = %s", (customerid,))
    customers_deleted = cur.rowcount
    mysql.connection.commit()
    cur.close()
    return customers_deleted

# delete vehicle
# DELETE not working :(
@app.route("/deletevehicle", methods=["GET", "POST"])
def delete_vehicle():
    if request.method == "POST":
        vehicleid = request.form["VehicleID"]
        if vehicleid:
            vehicles_deleted = delete_vehicle_in_db(vehicleid)
            if vehicles_deleted > 0:
                return render_template_string("""
                <b><p>Vehicle Data Deleted.</p></b>
                <p><a href="/mainmenu">Main Menu</a></p>
                """)
            else:
                return render_template_string("""
                <b><p>ID doesn't exist.</p></b>
                <p><a href="/deletevehicle">Go Back</a></p>
                """)
    return render_template_string("""
    <h1>Delete Vehicle</h1>
    <p><b>IMPORTANT</b>: Must delete the <b>rental</b> data associated by the deleted ID first. Otherwise, error will occur.</p>
    <form method="post" action="/deletevehicle?_method=DELETE">
        Find ID (Vehicle): <input type="text" name="VehicleID"><br>
        <button type="submit">Delete</button>
    </form>
    """)

def delete_vehicle_in_db(vehicleid):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM vehicle_rental.vehicles WHERE VehicleID = %s", (vehicleid,))
    vehicles_deleted = cur.rowcount
    mysql.connection.commit()
    cur.close()
    return vehicles_deleted

# search using id
@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        search_type = request.form["search_type"]
        search_id = request.form["search_id"]
        if not search_id:
            return render_template_string("""
            <h1>Search</h1>
            <form method="post">
                <label for="search_type">Search for:</label>
                <select name="search_type">
                    <option value="Customer">Customer</option>
                    <option value="Vehicle">Vehicle</option>
                    <option value="Rental">Rental</option>
                </select>
                <br>
                <label for="search_id">ID:</label>
                <input type="text" name="search_id"><br>
                <button type="submit">Search</button>
                <p style="color: red;">Field is empty</p>
                <p><a href="/mainmenu">Main Menu</a></p>
            </form>
            """)
        return redirect(url_for("search_results", search_type=search_type, search_id=search_id))
    
    return render_template_string("""
    <h1>Search</h1>
    <form method="post">
        <label for="search_type">Search for:</label>
        <select name="search_type">
            <option value="Customer">Customer</option>
            <option value="Vehicle">Vehicle</option>
            <option value="Rental">Rental</option>
        </select>
        <br>
        <label for="search_id">ID:</label>
        <input type="text" name="search_id"><br>
        <button type="submit">Search</button>
        <p><a href="/mainmenu">Main Menu</a></p>
    </form>
    """)

# search results with type of search and id
@app.route("/search/<search_type>/<search_id>", methods=["GET"])
def search_results(search_type, search_id):
    query = ""
    if search_type == "Customer":
        query = f"SELECT * FROM customers WHERE CustomerID = {search_id}"
    elif search_type == "Vehicle":
        query = f"SELECT * FROM vehicles WHERE VehicleID = {search_id}"
    elif search_type == "Rental":
        query = f"SELECT * FROM rentals WHERE RentalID = {search_id}"
    
    data = fetch_data(query)
    return make_response(jsonify(data), 200)

# run the program
if __name__ == "__main__":
    app.run(debug=True)