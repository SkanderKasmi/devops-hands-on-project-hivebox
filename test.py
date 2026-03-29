import  unittest
from app import getallboxesapi, datatemperaturevalidator, avg_temperature, return_version, app, __version__ 


# ______________________unit test declaration __________________________

class TestHiveBoxAPI(unittest.TestCase):
    """Unit tests for HiveBox API functions and endpoints"""
    def test_getallboxesapi(self):
        """test  getallboxesapi function"""
        response = getallboxesapi()
        self.assertIsInstance(response, list, "Response should be a list")
        self.assertGreater(len(response), 0, "Response should not be empty")

    def test_datatemperaturevalidator(self):
        """test datatemperaturevalidator function"""
        data = datatemperaturevalidator()
        self.assertIsInstance(data, list, "Data should be a list")
        for item in data:
            self.assertIn("box", item, "Each item should have a 'box' key")
            self.assertIn("temperature", item, "Each item should have a 'temperature' key")
            self.assertIsInstance(item["temperature"], (int, float), "Temperature should be a number")

    def test_avg_temperature(self):
        """test avg_temperature function"""
        data = avg_temperature()
        self.assertIsInstance(data, list, "Data should be a list")
        for item in data:
            self.assertIn("box", item, "Each item should have a 'box' key")
            self.assertIn("avg_temprature", item, "Each item should have an 'avg_temprature' key")
            self.assertIsInstance(item["avg_temprature"], (int, float), "Average temperature should be a number")

    def test_return_version(self):
        """test return_version function"""
        version = return_version()
        self.assertEqual(version, __version__, "Version should match the defined __version__")

    def test_getversion_api(self):
        """test /version API endpoint"""
        with app.test_client() as client:
            response = client.get("/version")
            self.assertEqual(response.status_code, 200, "Status code should be 200")
            data = response.get_json()
            self.assertIn("version", data, "Response should contain 'version' key")
            self.assertEqual(data["version"], __version__, "Version in response should match __version__")  

    def test_get_temperature_api(self):
        """test /temperature API endpoint"""
        with app.test_client() as client:
            response = client.get("/temperature")
            self.assertEqual(response.status_code, 200, "Status code should be 200")
            data = response.get_json()
            self.assertIn("Average Temperature", data, "Response should contain 'Average Temperature' key")
            for key in data["Average Temperature"]:
                self.assertIsInstance(key["avg_temprature"], (int, float), f"{key} should be a number")

    def  test_all(self):
        """run all tests"""
        self.test_getallboxesapi()
        self.test_datatemperaturevalidator()
        self.test_avg_temperature()
        self.test_return_version()
        self.test_getversion_api()
        self.test_get_temperature_api()                


if __name__ == "__main__":
    unittest.main()
    print("All tests passed!")