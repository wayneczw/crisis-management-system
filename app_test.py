import os
import unittest

from app import app

class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.APP = app.test_client()

    def test_map_psi(self):
        resp = self.APP.get('/map/psi')
        self.assertEqual(resp.status, '200 OK')

    def test_map_weather(self):
        resp = self.APP.get('/map/weather')
        self.assertEqual(resp.status, '200 OK')

    def test_map_shelters(self):
        resp = self.APP.get('/map/shelters')
        self.assertEqual(resp.status, '200 OK')

    def test_map_dengue(self):
        resp = self.APP.get('/map/dengue')
        self.assertEqual(resp.status, '200 OK')

if __name__ == '__main__':
    unittest.main()