import model


class MessageRenderer:
    """Base class for message renderer"""

    def render_message(self, incident: model.CrisisReport) -> str:
        raise NotImplementedError("render_message method not implemented")


class StubMessageRenderer(MessageRenderer):

    def render_message(self, incident: model.CrisisReport) -> str:
        return "Stub message"


class MessageFormatRenderer(MessageRenderer):
    """
    MessageFormatRenderer is a MessageRenderer that formats a string with an
    input parameter based on a predefined format_spec string
    """

    def __init__(self, format_spec: str):
        self.format_spec = format_spec

    def render_message(self, input) -> str:
        return self.format_spec.format(input)
