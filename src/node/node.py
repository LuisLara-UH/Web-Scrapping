import zmq

from zmq.sugar.frame import Message
from .utils import message
from .utils.tools import find_separator, get_current_ip
from .utils.node_reference import NodeReference
from .utils.sender import Sender

class Node():
    def __init__(self, listen_ip, listen_port, conn_node: NodeReference):
        # sender
        self.sender = Sender()
        # listening ip and port
        self.ip = listen_ip
        self.port = listen_port
        # connecting node address
        self.conn_node: NodeReference = conn_node
        self.chord_node = self.req_chord_node()

    def req_chord_node(self):
        msg = message.Message(action=message.GET_CHORD_NODE)
        rep_msg : message.Message = self.sender.request(conn_node=self.conn_node, msg=msg)

        if not rep_msg.action == message.RET_CHORD_NODE:
            raise Exception("Incorrect reply for chord node request")

        node_ref = NodeReference()
        node_ref.unpack(rep_msg.parameters)

        return node_ref

    def listen(self):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:" + self.port)

        while True:
            rcv_msg = message.Message()
            print('Listening from port ' + self.port + '...')
            rcv_msg.unpack(socket.recv_string())

            print('Received message:')
            rcv_msg.pprint()

            rep_msg: message.Message = self.read_msg(rcv_msg)
            socket.send_string(rep_msg.pack())
            print('Replied message:')
            rep_msg.pprint()

    def read_msg(self, msg: message.Message):
        if msg.action == message.GET_CHORD_NODE:
            return message.Message(action=message.RET_CHORD_NODE, parameters=self.chord_node.pack())
        return None
