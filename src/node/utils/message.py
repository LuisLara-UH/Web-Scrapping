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

GET_POST_SCRAP_NODE = 'get-set-scrap-node'
RET_POST_SCRAP_NODE = 'ret-set-scrap-node'

RET_EXCEPTION = 'ret-exc'

RET_NOT_REP = 'ret-not-rep'

GET_SET_URL = 'get-set-url'
RET_SET_URL = 'ret-set-url'

# Chord message protocols
GET_SUCC_KEY = 'get-succ-key'
RET_SUCC_KEY = 'ret-succ-key'

GET_SUCC_NODE = 'get-succ-node'
RET_SUCC_NODE = 'ret-succ-node'

GET_PRED_KEY = 'get-pred-key'
RET_PRED_KEY = 'ret-pred-key'

GET_PRED_NODE = 'get-pred-node'
RET_PRED_NODE = 'ret-pred-node'

GET_POST_FINGER = 'get-post-fing'
RET_POST_FINGER = 'ret-post-fing'

GET_SET_FINGER = 'get-set-fing'
RET_SET_FINGER = 'ret-set-fing'

GET_SCRAP_NODE = 'get-scrap-node'
RET_SCRAP_NODE = 'ret-scrap-node'

GET_POST_PRED = 'get-post-pred'
RET_POST_PRED = 'ret-post-pred'

GET_CHECK_NODE = 'get-check-node'
RET_CHECK_NODE = 'ret-check-node'

GET_POST_URL_DICT = 'get-post-url-dict'
RET_POST_URL_DICT = 'ret-post-url-dict'


class Message:
    def __init__(self, action: str = '', parameters: str = ''):
        self.action = action
        self.parameters = str(parameters)

    def pack(self):
        return self.action + '%' + self.parameters

    def unpack(self, msg: str):
        sep_index = find_separator(msg)

        if sep_index is None:
            raise Exception("Action separator in message received not found")

        self.action = msg[:sep_index]
        self.parameters = msg[sep_index + 1:]

    def pprint(self):
        print('Action: ' + self.action)
        print('Body: ' + self.parameters)


class ExceptionMessage(Message):
    def __init__(self):
        super().__init__(action=RET_EXCEPTION)
