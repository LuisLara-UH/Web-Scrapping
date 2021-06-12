GET_CHORD_NODE = 'get-chord'
RET_CHORD_NODE = 'ret-chord'

class Message():
    def __init__(self, action: str, parameters: str):
        self.action = action
        self.parameters = parameters

    def pack(self):
        return self.action + '%' + self.parameters

    def unpack(self, msg: str):
        sep_index = self.find_separator(msg)

        if sep_index is None:
            raise Exception("Action separator in message received not found")

        self.action = msg[:sep_index]
        self.parameters = msg[sep_index + 1:]

    def find_separator(self, text: str):
        index = 0
        while len(text) > index and not text[index] == '%':
            index += 1

        if len(text) == index:
            return None
        return index