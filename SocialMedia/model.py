from math import radians, cos, sin, asin, sqrt


class Priority:

    def __init__(self, injury_value, danger_value, help_value):
        self.injury = injury_value
        self.danger = danger_value
        self.help = help_value


class Report:

    def __init__(self, identifier, name, address):
        self.identifier = identifier
        self.name = name
        self.address = address


class IncidentReport(Report):

    def __init__(self, identifier, name, address, phone, description, status, reported_time, assistance_required,
                 priority):
        super().__init__(identifier, name, address)
        self.phone = phone
        self.address = address
        self.description = description
        self.status = status
        self.reported_time = reported_time
        self.assistance_required = assistance_required
        self.priority = priority


class CrisisReport(Report):

    def __init__(self, identifier, name, address, category, description, date, time, advisory):
        super().__init__(identifier, name, address)
        self.category = category
        self.address = address
        self.description = description
        self.date = date
        self.time = time
        self.advisory = advisory


class Contact:
    AUTHORITY_POLICE = 0

    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

    @staticmethod
    def retrieve_authority_contact(authority):
        if authority == Contact.AUTHORITY_POLICE:
            return Contact('Police', '+6591515341')
        else:
            raise ValueError("Authority is undefined")


class Person(Contact):
    GENDER_MALE = 'M'
    GENDER_FEMALE = 'F'

    def __init__(self, name, phone, gender, address):
        super().__init__(name, phone)
        self.gender = gender
        self.address = address

    @staticmethod
    def retrieve_nearby_residents(coordinate, max_distance):
        """
        Retrieve nearby residents
        :param coordinate: The anchor point coordinate to search for nearby residents
        :param max_distance: The maximum distance allowed from the anchor point
        :return: A list of nearby residents
        """

        person_list = [
            Person("Tan Ying Hao", '+6591515341', Person.GENDER_MALE,
                   Address('Blk 540 Jelepang Road', '20-36', '670540',
                           GeoCoordinate(1.384860, 103.766550))),
            Person("Lim Xuan Yin", '+6591116528', Person.GENDER_MALE,
                   Address('Blk 487 Tampines Street Avenue 4', '03-99', '520487',
                           GeoCoordinate(1.360320, 103.944397)))
        ]

        nearby = []
        for person in person_list:
            if person.address.coordinates.calculate_distance(coordinate) <= max_distance:
                nearby.append(person)

        return nearby


class Address:

    def __init__(self, street_name, unit_number, postal_code, coordinates):
        self.street_name = street_name if street_name is not None else ''
        self.unit_number = unit_number if unit_number is not None else ''
        self.postal_code = postal_code if postal_code is not None else ''
        self.__coordinates__ = coordinates

    @property
    def coordinates(self):
        if self.__coordinates__ is not None:
            return self.__coordinates__
        else:
            return GeoCoordinate(1.384860, 103.766550)


class GeoCoordinate:

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def calculate_distance(self, destination):
        """
        Calculates the distance from the this coordinate to the specified destination
        :param destination: The destination coordinate
        :return: A float value indicating the distance between this coordinate and destination in kilometres
        """

        lon1, lat1, lon2, lat2 = map(radians, [self.longitude, self.latitude,
                                               destination.longitude, destination.latitude])

        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))

        return c * 6371
