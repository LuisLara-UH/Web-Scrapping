from .utils import message
from .utils.tools import find_separator

class NodeReference():
    def __init__(self, ip = None, port = None):
        self.ip = ip
        self.port = port

    def pack(self):
        return self.ip + '%' + self.port

    def unpack(self, text: str):
        index = find_separator(text)


class Node():
    def __init__(self, list_port, conn_node: NodeReference):
        # listening port
        self.port = list_port
        # connecting node address
        self.conn_node: NodeReference = conn_node
        self.chord_node = self.req_chord_node()

    def req_chord_node(self):
        msg = message.Message(action=message.GET_CHORD_NODE)
        rep_msg : message.Message = self.request(conn_node=self.conn_node, msg=msg)

        if not rep_msg.action == message.RET_CHORD_NODE:
            raise Exception("Uncorrect reply for chord node request")

    def get_chord_node(self):
        return self.chord_node

    def listen(self):
        raise NotImplementedError()

    def request(self, conn_node: NodeReference, msg: message.Message) -> message.Message:
        pass

