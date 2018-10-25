from twilio.rest import Client
from facebook import GraphAPI


class APIConnector:
    """Base class for API connectors"""

    def send_message(self, message: str, **kwargs):
        raise NotImplementedError("send_message method is not implemented")


class SMSConnector(APIConnector):
    """SMSConnector is an APIConnector that performs communication with the SMS API"""

    def __init__(self):
        self.sandbox_number = '+12702322436'
        self.client = Client('AC9c4f708b31ffc68d3d82affe859df061',
                             '5c17b294472393c6713408212aa9e00b')

    def send_message(self, message: str, recipient_number: int):
        """
        Sends a message to the SMS API
        :param message: A text string message to be sent to the SMS API
        :param recipient_number: The phone number to indicate to the SMS API
        :return: None
        """

        self.client.messages.create(body=message,
                                    from_=self.sandbox_number,
                                    to=recipient_number)


class FacebookConnector(APIConnector):
    """FacebookConnector is an APIConnector that performs communication with the Facebook API"""

    def __init__(self):
        self.page_id = '570688683390106'
        self.access_token = 'EAACfoaUxqb8BAGM8c39Nh' \
                    'WHUXREdmf210WhzVCXr3CJ' \
                    'BFGQUu1EtyHihOcKuwYgM4' \
                    '3Vd98TTlctN2ZBFJmU9uqo' \
                    '5iQZBXIZB3TH9RdZC9luy2' \
                    'skvxabhajpA694D6uJvl6t' \
                    'c4EK7Mp4levQW5UDnwj1bg' \
                    'EBXsplkAZBZCXk8mqebJYT' \
                    'pQAvTLNmxP68f449wOoKKP' \
                    '3On2bYQZDZD'
        self.client = GraphAPI(access_token=self.access_token)

    def send_message(self, message: str):
        """
        Sends a message to the Facebook API
        :param message: A text string message to be sent to the Facebook API
        :return: None
        """

        self.client.put_object(self.page_id, 'feed', message=message)
