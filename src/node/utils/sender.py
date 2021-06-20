import zmq
from zmq.sugar.poll import Poller, POLLIN

from .node_reference import NodeReference
from .message import Message, RET_EXCEPTION, RET_NOT_REP


class Sender:
    def request(self, conn_node: NodeReference, msg: Message, wait_time: int = 3000):
        context = zmq.Context()
        socket = context.socket(zmq.DEALER)
        socket.connect(f"tcp://{conn_node.ip}:{conn_node.port}")
        socket.send_string(msg.pack())
        rep_msg = Message()
        print('Sending1')
        poller = Poller()
        poller.register(socket=socket, flags=POLLIN)
        print('Sending2')
        ready = dict(poller.poll(wait_time))
        print('Sending3')

        if ready:
            print('Sending4')
            rep_msg.unpack(socket.recv_multipart()[0].decode())
            print('Sending5')
        else:
            print('Sending6')
            rep_msg = Message(action=RET_NOT_REP)
        socket.close()

        assert not rep_msg.action == RET_EXCEPTION, 'An exception occurred in calling node'
        print('Sending7')
        print(rep_msg.action)
        return rep_msg
