import unittest
from .. import model
from ..controller import SocialMedia


class SocialMediaTest(unittest.TestCase):

    def test_alert_authorities_test(self):
        """Test case 1"""

        controller = SocialMedia()
        controller.alert_authorities(model.IncidentReport(0, "Incident 1",
                                                          model.Address('101 Bukit Panjang Road', None, '679910',
                                                                        model.GeoCoordinate(1.360320, 103.944397)),
                                                          "+6591515341",
                                                          "This is a description of the crisis",
                                                          "5",
                                                          "14-Jul-1993 09:30", "No assistance required",
                                                          model.Priority(5, 3, 7)),
                                     model.Contact.AUTHORITY_POLICE)
        self.assertTrue(True)

    def test_alert_public_test(self):
        """Test case 2"""

        controller = SocialMedia()
        controller.alert_public(model.CrisisReport(0, "Fire at ABC",
                                                   model.Address('101 Bukit Panjang Road', None, '679910',
                                                                 model.GeoCoordinate(1.360320, 103.944397)),
                                                   "Fire", "Big fire at CDE", "14-07-1993", "10:30", "Do not panic"))
        self.assertTrue(True)

    def test_post_facebook_test(self):
        """Test case 3"""

        controller = SocialMedia()
        controller.post_facebook(model.CrisisReport(0, "Fire at ABC",
                                                    model.Address('101 Bukit Panjang Road', None, '679910',
                                                                  model.GeoCoordinate(1.360320, 103.944397)),
                                                    "Fire", "Big fire at CDE", "14-07-1993", "10:30", "Do not panic"))
        self.assertTrue(True)
