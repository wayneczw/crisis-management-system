import model
import renderer
import connector

ALERT_AUTHORITY_SPEC = """
Crisis Management System

The following incident was recorded and assistance is required from your department.

*Incident ID*
{0.identifier}

*Reported Time*
{0.reported_time}

*Caller Name* 
{0.name}

*Caller Phone*
{0.phone}

*Address*
{0.address.street_name} {0.address.unit_number}
{0.address.postal_code}

*Description*
{0.description}

*Assistance Required*
{0.assistance_required}

*Priority Values*
Injury: {0.priority.injury}
Danger: {0.priority.danger}
Help:{0.priority.help}
"""

ALERT_PUBLIC_SPEC = """
Public Alert Message
        
This is a public alert message to inform you 
that an incident has occurred on {0.date} {0.time} 
in the vicinity of your residential area, 
please follow the advisory stated below on any possible 
follow-up actions.
        
Incident Name: 
{0.name}

Incident Category: 
{0.category}
        
Description:
{0.description}
        
Advisory:
{0.advisory}
"""


class SocialMedia:

    def __init__(self):
        self.alert_authority_renderer = renderer.MessageFormatRenderer(ALERT_AUTHORITY_SPEC)
        self.alert_public_renderer = renderer.MessageFormatRenderer(ALERT_PUBLIC_SPEC)

        self.facebook_connector = connector.FacebookConnector()
        self.sms_connector = connector.SMSConnector()

    def alert_authorities(self, incident: model.IncidentReport, authority):
        self.sms_connector.send_message(self.alert_authority_renderer.render_message(incident),
                                        model.Contact.retrieve_authority_contact(authority).phone)

    def alert_public(self, incident: model.CrisisReport, max_distance_km=5):
        public_members = model.Person.retrieve_nearby_residents(incident.coordinate, max_distance_km)
        for member in public_members:
            self.sms_connector.send_message(self.alert_public_renderer.render_message(incident), member.phone)

    def post_facebook(self, incident: model.CrisisReport):
        self.facebook_connector.send_message(self.renderer.render_message(incident))


def alert_authorities_test():
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


def alert_public_test():
    controller = SocialMedia()
    controller.alert_public(model.CrisisReport())


def post_facebook_test():
    controller = SocialMedia()
    controller.post_facebook(model.CrisisReport())


if __name__ == "__main__":
    alert_authorities_test()
    # alert_public_test(incident_obj)
    # post_facebook_test(incident_obj)
