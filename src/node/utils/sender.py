import zmq
from zmq.sugar.poll import Poller, POLLIN

from .node_reference import NodeReference
from .message import Message, RET_EXCEPTION, RET_NOT_REP


class Sender:
    def __init__(self):
        self.context = zmq.Context()
        self.poller = Poller()

    def request(self, conn_node: NodeReference, msg: Message, wait_time: int = 180000):
        socket = self.context.socket(zmq.DEALER)
        socket.connect(f"tcp://{conn_node.ip}:{conn_node.port}")
        socket.send_string(msg.pack())
        rep_msg = Message()
        self.poller.register(socket=socket, flags=POLLIN)
        ready = dict(self.poller.poll(wait_time))

        if ready:
            rep_msg.unpack(socket.recv_multipart()[0].decode())
        else:
            rep_msg = Message(action=RET_NOT_REP)
        socket.close()
        self.poller.unregister(socket)

        assert not rep_msg.action == RET_EXCEPTION, 'An exception occurred in calling node'
        return rep_msg
