# Python Flask CRUD REST API Project with Database

## Vehicle Rental Database API Project

### Project Details
This project is a simple Flask application that serves as a vehicle rental database. It allows users to perform CRUD (Create, Read, Update, Delete) operations on customers, vehicles, and rental information.

There are two files associated with this project:
`api.py`: this is with HTML implementation. 
`api_client.py`: this is only with the use of a client tool.

### Installation
1. Download the Python files in the repository.
2. Import the `VehicleRental.sql` to your MySQL Workbench.
3. Install dependencies (preferably in a virtual environment): `pip install  flask-mysqldb` and `pip install flask`
4. Run the Python files.

## Usage Examples
### For `api.py`:
1. Run the Flask application in your IDE, or in a Command Prompt: `python api.py`.
2. Access the HTML site by typing `http://127.0.0.1:5000/mainmenu`.
3. Navigate through the menu to perform various operations such as adding customers, vehicles, rentals, updating data, and deleting data.

### For `api_client.py`:
1. Run the Flask application in your IDE, or in a Command Prompt: `python api_client.py`.
2. Access the app by using client tools (ex: **Postman**). 
3. Type the HTML site to the **"Enter URL or paste text"** box.
4. Change the request method (default: **GET**) to the left of the URL box of your method of your choice.

**Examples**
*GET*: `http://127.0.0.1:5000/customers/`
*POST*: `http://127.0.0.1:5000/customers/` then go to *Body*, set it to "raw" change "Text" to "JSON", then enter this:

    {
	    "CustomerName": "your_name",
	    "ContactNumber": "09123456789"
    }

*PUT*: `http://127.0.0.1:5000/customers/`, replace your entered input to this:

    {
	    "CustomerName": "new_name",
	    "ContactNumber": "09876543210"
    }

*DELETE*: `http://127.0.0.1:5000/customers/*ID you want to delete*`
Example: `http://127.0.0.1:5000/customers/20`

### For `test.py`:
1. Run the Flask application in your IDE, or in a Command Prompt: `python api_client.py`.
2. Run the `test.py` afterwards. *You can **examine** the codes first before running the Python file.*
4. Change the information inside the double quotes you want to test.

**IMPORTANT NOTE**: When running this Python file, use **ONE** function (`def ():`) at a time by commenting the rest of the functions **EXCEPT** the `def setUp(self):`function.

## API Usage (`api.py`)
- **GET `/mainmenu`**: Displays the main menu of the application.
- **GET `/database`**: Retrieves the entire database in JSON format.
- **POST `/addcustomer`**: Adds a new customer to the database.
- **POST `/addrental`**: Adds a new rental information to the database.
- **POST `/addvehicle`**: Adds a new vehicle to the database.
- **POST `/updatecustomer`**: Updates customer information in the database.
- **POST `/updatevehicle`**: Updates vehicle information in the database.
- **POST `/updaterental`**: Updates rental information in the database.
- **POST `/deleterental`**: Deletes rental information from the database.
- **POST `/deletecustomer`**: Deletes customer information from the database.
- **POST `/deletevehicle`**: Deletes vehicle information from the database.
- **POST `/search`**: Searches for data in the database based on the provided ID and type (customer, vehicle, or rental).

**IMPORTANT NOTE:** Some functionalities like PUT (`/update`) and DELETE (`/delete`) requests are replaced because HTML don't support these methods by default.

---
## API Usage (`api_client.py`)
- **GET `/mainmenu`**: Displays the main menu of the application.
- **GET `/database`**: Retrieves the entire database in JSON format.
- **POST `/addcustomer`**: Adds a new customer to the database.
- **POST `/addrental`**: Adds a new rental information to the database.
- **POST `/addvehicle`**: Adds a new vehicle to the database.
- **PUT `/updatecustomer`**: Updates customer information in the database.
- **PUT `/updatevehicle`**: Updates vehicle information in the database.
- **PUT `/updaterental`**: Updates rental information in the database.
- **DELETE `/deleterental`**: Deletes rental information from the database.
- ***DELETE `/deletecustomer`**: Deletes customer information from the database.
- ***DELETE `/deletevehicle`**: Deletes vehicle information from the database.
---