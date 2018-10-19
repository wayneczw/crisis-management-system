from twilio.rest import Client


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

    def send_message(self, message: str):
        """
        Sends a message to the Facebook API
        :param message: A text string message to be sent to the Facebook API
        :return: None
        """
        raise NotImplementedError("send_message method is not implemented")
