from .node import Node, NodeReference
from .utils import message
from .utils.tools import get_current_ip
from .utils.chord_utils import *
from .utils.node_reference import Finger
from .utils.codifiers import *
from .utils.chord_messages import *

class ChordNode(Node):
    def __init__(self, listen_ip, listen_port, conn_node: NodeReference):
        super().__init__(listen_ip, listen_port, conn_node)

        self.m = 128
        self.id = get_node_id(self.ip + self.port)
        self.my_finger = Finger(self.ip, self.port, self.id)
        self.successor = None
        self.predecessor = None
        self.finger_table = [None] * self.m

        self.join()

    def join(self):
        self.init_finger_table()
        self.update_others()

    def get_chord_node(self):
        return NodeReference(ip=get_current_ip(), port=self.port)

    def read_msg(self, msg: message.Message):
        ret_msg = super().read_msg(msg)
        if not ret_msg is None:
            return ret_msg

        if msg.action == GET_CHORD_URL:
            return self.get_url_info(msg.parameters)
        
        if msg.action == GET_POST_FINGER:
            return self.ask_set_finger(msg.parameters)
        
        if msg.action == GET_SUCC_KEY:
            return self.get_succ_key(msg.parameters)

        if msg.action == GET_SUCC_NODE:
            return self.get_succ_node()

        if msg.action == GET_PRED_KEY:
            return self.get_pred_key(msg.parameters)

        if msg.action == GET_PRED_NODE:
            return self.get_pred_node()

        if msg.action == GET_SET_FINGER:
            return self.set_finger(msg.parameters)

        return Message(action='')

    def init_finger_table(self):
        for i in range(0, self.m):
            self.finger_table[i] = self.my_finger

        if self.conn_node is None:
            return

        # request my successor from known node
        self.finger_table[1] = req_succ_of_key(sender=self.sender, conn_node=self.conn_node, key=self.id)
        # set my predecessor as my successor's predecessor
        self.finger_table[0] = req_pred_of_key(
            sender=self.sender, conn_node=self.conn_node, key=self.successor.id
        )
        # I'm my successors predecessor
        req_set_finger(sender=self.sender, conn_node=self.successor(), finger=self.my_finger, pos=0)

        for i in range(1, self.m - 1):
            if belongs_to_interval(finger_number(self.id, i + 1), self.id, self.finger_table[i]):
                self.finger_table[i + 1] = self.finger_table[i]
            else:
                succ_node = req_succ_of_key(sender=self.sender, conn_node=self.conn_node, key=finger_number(self.id, i + 1))
                if not belongs_to_interval(succ_node.id, finger_number(self.id, i + 1), self.id):
                    succ_node = self.my_finger
                self.finger_table[i + 1] = succ_node

    def predecessor(self) -> Finger:
        return self.finger_table[0]

    def successor(self) -> Finger:
        return self.finger_table[1]

    def update_others(self):
        for i in range(1, self.m):
            pred = self.find_predecessor(self.id - 2 ^ (i - 1))
            if not self.my_finger.same_ref(pred):
                req_post_finger(sender=self.sender, conn_node=pred, finger=self.my_finger)

    def find_predecessor(self, id: int):
        if self.successor().id == self.id or belongs_to_interval(id, self.id, self.successor().id):
            return self.my_finger

        index = 1
        while self.finger_table[index + 1] < id:
            index += 1

        return req_pred_of_key(sender=self.sender, conn_node=self.finger_table[index], key=id)

    def find_successor(self, id: int):
        pred_node = self.find_predecessor(id)
        return get_succ_of_node(sender=self.sender, conn_node=pred_node)

    def closest_preceding_finger(self, id: int):
        for i in range(self.m - 1, 0, -1):
            if belongs_to_open_interval(self.finger_table[i].id, self.id, id):
                return self.finger_table[i]
        return self.my_finger

    # response to messages
    def get_url_info(self, url: str) -> Message:
        # Temporal
        return ret_url_info('Url info')

    def ask_set_finger(self, params: str) -> Message:
        finger, pos = decode_post_finger(params)
        if self.finger_table[pos].id > finger.id:
            self.finger_table[pos] = finger
        return ret_post_finger()

    def get_pred_key(self, key: str) -> Message:
        pred_node = self.find_predecessor(int(key))
        return ret_pred_of_key(pred_node)

    def get_pred_node(self) -> Message:
        return ret_pred_of_node(self.predecessor())

    def set_finger(self, params: str) -> Message:
        finger, pos = decode_post_finger(params)
        self.finger_table[pos] = finger
        return ret_set_finger()

    def get_succ_key(self, key: str) -> Message:
        succ_node = self.find_successor(int(key))
        return ret_succ_of_key(succ_node)

    def get_succ_node(self) -> Message:
        return ret_succ_of_node(self.successor())

