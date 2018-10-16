import unittest
from ..map_api import get_dengue_clusters, get_psi, get_shelter, get_weather, address_to_latlng

class TestMapApi(unittest.TestCase):

    def test_get_dengue_clusters(self):
        dengue_clusters = get_dengue_clusters()
        self.assertIsNotNone(dengue_clusters)

    def test_get_psi(self):
        psi = get_psi()
        self.assertIsNotNone(psi)

    def test_get_shelter(self):
        shelter = get_shelter()
        self.assertIsNotNone(shelter)

    def test_get_weather(self):
        weather = get_weather()
        self.assertIsNotNone(weather)

    def test_address_to_latlng(self):
        address = 'Nanyang Technological University, Singapore'
        latlng = address_to_latlng(address)
        self.assertIsNotNone(latlng)
