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
        self.assertEqual(response.data.decode(), "<p>Hello World</p>")

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

if __name__ == "__main__":
    unittest.main()