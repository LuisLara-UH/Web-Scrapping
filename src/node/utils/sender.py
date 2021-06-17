import zmq

from .node_reference import NodeReference
from .message import Message, RET_EXCEPTION

class Sender():
    def request(self, conn_node: NodeReference, msg: Message):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect(f"tcp://{conn_node.ip}:{conn_node.port}")
        socket.send_string(msg.pack())
        rep_msg = Message()
        rep_msg.unpack(socket.recv_string())
        socket.close()

        assert not rep_msg.action == RET_EXCEPTION, 'An exception ocurred in calling node'

        return rep_msg