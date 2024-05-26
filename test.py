import unittest
import warnings
from api import app

class MyAppTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()
        warnings.simplefilter("ignore", category=DeprecationWarning)

    def test_index_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "")

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

    def test_update_customer(self):
        response = self.app.put(
            "/customers/1",
            json={"CustomerName": "Updated Name", "ContactNumber": "1234567890"}
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue("Customer Updated!" in response.json["Message"])

    def test_update_vehicle(self):
        response = self.app.put(
            "/vehicles/1",
            json={"ManufacturerVehicle": "Updated Manufacturer", "VehicleModel": "Updated Model", "DailyRate": 100.00}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Vehicle Updated!" in response.json["Message"])

    def test_update_rental(self):
        response = self.app.put(
            "/rentals/1",
            json={"CustomerID": 1, "VehicleID": 1, "RentalStatus": "Updated Status", "StartDate": "2024-01-01", "EndDate": "2024-12-31"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Rental Updated!" in response.json["Message"])

    def test_delete_customer(self):
        response = self.app.delete("/customers/1")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Customer Deleted!" in response.json["Message"])

    def test_delete_vehicle(self):
        response = self.app.delete("/vehicles/1")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Vehicle Deleted!" in response.json["Message"])

    def test_delete_rental(self):
        response = self.app.delete("/rentals/1")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Rental Deleted!" in response.json["Message"])

if __name__ == "__main__":
    unittest.main()