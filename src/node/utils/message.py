from .tools import find_separator

# General message protocols
GET_CHORD_NODE = 'get-chord'
RET_CHORD_NODE = 'ret-chord'

GET_URL_INFO = 'get-url'
RET_URL_INFO = 'ret-url'

GET_SCRAP_URL = 'get-scrap'
RET_SCRAP_URL = 'ret-scrap'

GET_CHORD_URL = 'get-chord-url'
RET_CHORD_URL = 'ret-chord-url'

# Chord message protocols
GET_SUCC_KEY = 'get-succ-key'
RET_SUCC_KEY = 'ret-succ-key'

GET_SUCC_NODE = 'get-succ-node'
RET_SUCC_NODE = 'ret-succ-node'

GET_PRED_NODE = 'get-pred'
RET_PRED_NODE = 'ret-pred'

GET_POST_FINGER = 'get-post-fing'
RET_POST_FINGER = 'ret-post-fing'

GET_SET_FINGER = 'get-set-fing'
RET_SET_FINGER = 'ret-set-fing'

class Message():
    def __init__(self, action: str = '', parameters: str = ''):
        self.action = action
        self.parameters = parameters

    def pack(self):
        return self.action + '%' + self.parameters

    def unpack(self, msg: str):
        sep_index = find_separator(msg)

        if sep_index is None:
            raise Exception("Action separator in message received not found")

        self.action = msg[:sep_index]
        self.parameters = msg[sep_index + 1:]