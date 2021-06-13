from zmq.sugar.frame import Message
from .utils import message
from .utils.tools import find_separator
import zmq

class NodeReference():
    def __init__(self, ip = None, port = None):
        self.ip = ip
        self.port = port

    def pack(self):
        return self.ip + '%' + self.port

    def unpack(self, text: str):
        index = find_separator(text)
        self.ip = text[:index]
        self.port = text[index + 1:]


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
            raise Exception("Incorrect reply for chord node request")

        node_ref = NodeReference()
        node_ref.unpack(rep_msg.parameters)

        return node_ref

    def listen(self):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*" + self.port)

        while True:
            rcv_msg = message.Message()
            rcv_msg.unpack(socket.recv_string())

            rep_msg: message.Message = self.read_msg(rcv_msg)
            socket.send_string(rep_msg)

    def read_msg(self, msg: message.Message):
        if msg.action == message.GET_CHORD_NODE:
            return message.Message(action=message.RET_CHORD_NODE, parameters=self.chord_node.pack())
        return None
         
    def request(self, conn_node: NodeReference, msg: message.Message):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect(f"tcp://{conn_node.ip}:{conn_node.port}")
        socket.send_string(msg.pack())
        rep_msg = message.Message()
        rep_msg.unpack(socket.recv_string())
        socket.close()

        return rep_msg

