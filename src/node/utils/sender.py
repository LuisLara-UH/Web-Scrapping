import zmq

from .node_reference import NodeReference
from .message import Message

class Sender():
    def request(self, conn_node: NodeReference, msg: Message):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect(f"tcp://{conn_node.ip}:{conn_node.port}")
        socket.send_string(msg.pack())
        rep_msg = Message()
        rep_msg.unpack(socket.recv_string())
        socket.close()

        return rep_msg