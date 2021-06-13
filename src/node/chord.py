from .node import Node, NodeReference
from .utils import message
from .utils import tools

class ChordNode(Node):
    def __init__(self, list_port, conn_node: NodeReference):
        super().__init__(list_port, conn_node)

    def get_chord_node(self):
        return NodeReference(ip=tools.get_current_ip(), port=self.port)

    def read_msg(self, msg: message.Message):
        ret_msg = super().read_msg(msg)
        if not ret_msg is None:
            return ret_msg

        # fill
