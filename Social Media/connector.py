from twilio.rest import Client


class APIConnector:

    def send_message(self, message: str, **kwargs):
        raise NotImplementedError("send_message method is not implemented")


class SMSConnector(APIConnector):

    def __init__(self):
        self.sandbox_number = '+12702322436'
        self.client = Client('AC9c4f708b31ffc68d3d82affe859df061',
                             '5c17b294472393c6713408212aa9e00b')

    def send_message(self, message: str, recipient_number: int):
        self.client.messages.create(body=message,
                                    from_=self.sandbox_number,
                                    to=recipient_number)


class FacebookConnector(APIConnector):

    def send_message(self, message: str):
        raise NotImplementedError("send_message method is not implemented")
