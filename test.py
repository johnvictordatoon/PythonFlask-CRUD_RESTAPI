import unittest
import warnings
from api_client import app

class MyAppTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()
        warnings.simplefilter("ignore", category=DeprecationWarning)

    def test_index_page(self):
        response = self.app.get("/mainmenu")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "<h1>Vehicle Rental Database</h1>")

    def test_getvehicles(self):
        response = self.app.get("/vehicles")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Lamborghini" in response.data.decode())

    def test_getvehiclesbyid(self):
        response = self.app.get("/vehicles/5")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Lamborghini" in response.data.decode())

    def test_get_dailyrate_by_vehicles(self):
        response = self.app.get("/vehicles/daily_rate")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("5000.00" in response.data.decode())

    def test_get_rentals(self):
        response = self.app.get("/rentals")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Cancelled" in response.data.decode())

    def test_get_rentalsbyid(self):
        response = self.app.get("/rentals/1")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Confirmed" in response.data.decode())

    def test_get_rentalstatus(self):
        response = self.app.get("/rentals/rental_status")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Confirmed" in response.data.decode())

    def test_add_customer(self):
        response = self.app.post(
            "/customers",
            json={"CustomerName": "Alden Richards", "ContactNumber": "09886544200"}
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue("New Customer Added!" in response.json["Message"])

    def test_add_vehicle(self):
        response = self.app.post(
            "/vehicles",
            json={"ManufacturerVehicle": "Bugatti", "VehicleModel": "Veyron Super Sport", "DailyRate": 40000.00}
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue("New Vehicle Added!" in response.json["Message"])

    def test_add_rental(self):
        response = self.app.post(
            "/rentals",
            json={"CustomerID": 30, "VehicleID": 28, "RentalStatus": "Pending", "StartDate": "2024-04-04", "EndDate": "2024-05-21"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Rental Added!" in response.json["Message"])

    def test_update_customer(self):
        response = self.app.put(
            "/customers/30",
            json={"CustomerName": "Alden 'Pal'wan' Richards", "ContactNumber": "09886544200"}
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue("Customer Updated!" in response.json["Message"])

    def test_update_vehicle(self):
        response = self.app.put(
            "/vehicles/28",
            json={"ManufacturerVehicle": "Ford", "VehicleModel": "Focus", "DailyRate": 2500.00}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Vehicle Updated!" in response.json["Message"])

    def test_update_rental(self):
        response = self.app.put(
            "/rentals/28",
            json={"CustomerID": 30, "VehicleID": 28, "RentalStatus": "Cancelled", "StartDate": "2024-04-04", "EndDate": "2024-05-21"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Rental Updated!" in response.json["Message"])

    def test_delete_rental(self):
        response = self.app.delete("/rentals/28")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Rental Deleted!" in response.json["Message"])

    def test_delete_customer(self):
        response = self.app.delete("/customers/30")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Customer Deleted!" in response.json["Message"])

    def test_delete_vehicle(self):
        response = self.app.delete("/vehicles/28")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Vehicle Deleted!" in response.json["Message"])

if __name__ == "__main__":
    unittest.main()