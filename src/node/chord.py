from threading import Thread
from .node import Node, NodeReference
from .utils import message
from .utils.tools import get_current_ip
from .utils.chord_utils import *
from .utils.node_reference import Finger
from .utils.codifiers import *
from .utils.chord_messages import *
import time
import random

class ChordNode(Node):
    def __init__(self, listen_ip, listen_port, conn_node: NodeReference):
        super().__init__(listen_ip, listen_port, conn_node)

        self.id = get_hash(self.ip + self.port)
        print('Id: ', self.id)
        self.my_finger = Finger(self.ip, self.port, self.id)
        self.dict_url = {}
        self.finger_table = [None] * (m + 1)
        self.scrapper_nodes = []

        self.join()

    def join(self):
        for i in range(0, m + 1):
            self.finger_table[i] = self.my_finger

        if self.conn_node:
            print('Initialize finger table...')
            self.init_finger_table()
            print('Finger table initialized. Updating other nodes...')
            self.update_others()
            print('Other nodes updated')

    def stabilize(self):
        while True:
            if not self.successor().same_ref(self.my_finger):
                succ_pred = get_pred_of_node(self.sender, self.successor())
                if belongs_to_interval(succ_pred.id, self.id, self.successor().id):
                    self.finger_table[1] = succ_pred
                req_post_pred(self.sender, self.successor(), self.my_finger)

            time.sleep(3)

    def fix_fingers(self):
        while True:
            i = random.randint(2, m)
            succ_node = self.find_successor(finger_number(self.id, i))
            if not belongs_to_interval(succ_node.id, finger_number(self.id, i), self.id):
                succ_node = self.my_finger
            self.finger_table[i] = succ_node

            time.sleep(3)

    def req_chord_node(self):
        return self.get_chord_node()

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

        if msg.action == GET_SCRAP_NODE:
            return self.get_scrapper_node(msg.parameters)

        if msg.action == GET_POST_SCRAP_NODE:
            self.ask_add_scrap_node(msg.parameters)
            return ret_post_scrap_node()

        if msg.action == GET_POST_PRED:
            return self.notify_predecessor(msg.parameters)

        if msg.action == GET_SET_URL:
            self.set_url_info(url_pack=msg.parameters)
            return ret_set_url()

        return Message(action='')

    def init_finger_table(self):
        # request my successor from known node
        self.finger_table[1] = req_succ_of_key(sender=self.sender, conn_node=self.conn_node, key=self.id)
        print('Successor: ' + str(self.finger_table[1].id))
        # set my predecessor as my successor's predecessor
        self.finger_table[0] = get_pred_of_node(sender=self.sender, conn_node=self.successor())
        print('Predecessor: ' + str(self.finger_table[0].id))
        # I'm my successors predecessor
        req_set_finger(sender=self.sender, conn_node=self.successor(), finger=self.my_finger, pos=0)

        print('Initializing fingers...')
        for i in range(1, m):
            if belongs_to_interval(finger_number(self.id, i + 1), self.id, self.finger_table[i].id):
                self.finger_table[i + 1] = self.finger_table[i]
            else:
                succ_node = self.find_successor(finger_number(self.id, i + 1))
                if not belongs_to_interval(succ_node.id, finger_number(self.id, i + 1), self.id):
                    succ_node = self.my_finger
                self.finger_table[i + 1] = succ_node
            print(str(i + 1) + ' finger initialized. Value: ' + str(self.finger_table[i + 1].id))

    def predecessor(self) -> Finger:
        return self.finger_table[0]

    def successor(self) -> Finger:
        return self.finger_table[1]

    def update_others(self):
        for i in range(1, m + 1):
            pred = self.find_predecessor(chord_number(self.id - 2 ** (i - 1)))
            if not self.my_finger.same_ref(pred):
                req_post_finger(sender=self.sender, conn_node=pred, finger=self.my_finger, pos=i)

    def find_predecessor(self, id: int):
        if self.successor().id == self.id or belongs_to_interval(id, self.id, self.successor().id):
            return self.my_finger

        index = m - 1
        while not belongs_to_interval(self.finger_table[index].id, self.id, id):
            index -= 1

        return req_pred_of_key(sender=self.sender, conn_node=self.finger_table[index], key=id)

    def find_successor(self, id: int):
        pred_node = self.find_predecessor(id)
        if pred_node.same_ref(self.my_finger):
            return self.successor()
        return get_succ_of_node(sender=self.sender, conn_node=pred_node)

    def closest_preceding_finger(self, id: int):
        for i in range(m - 1, 0, -1):
            if belongs_to_open_interval(self.finger_table[i].id, self.id, id):
                return self.finger_table[i]
        return self.my_finger

    # response to messages
    def get_url_info(self, url: str) -> Message:
        url_hash: int = get_hash(url)
        url_info = ''
        if belongs_to_interval(url_hash, self.predecessor().id, self.id):
            try:
                return ret_url_info(self.dict_url[url_hash])
            except KeyError:
                if len(self.scrapper_nodes) == 0:
                    my_ref = NodeReference(self.ip, self.port)
                    self.get_scrapper_node(my_ref.pack())
                
                assert len(self.scrapper_nodes) > 0, 'No scrapper nodes found'
                url_info = req_scrap_url(sender=self.sender, conn_node=self.scrapper_nodes[0], url=url)
                self.dict_url[url_hash] = url_info
        else:
            successor = self.find_successor(id=url_hash)
            url_info = req_chord_url(self.sender, successor, url)

        return ret_url_info(url_info=url_info)

    def get_scrapper_node(self, sender_node: str) -> Message:
        sender = NodeReference()
        sender.unpack(sender_node)

        if len(self.scrapper_nodes) > 0:
            return ret_scrapper_node(self.scrapper_nodes[0])

        assert not sender.same_ref(self.successor()), 'Scrapper node not found'
        scrapper = req_scrapper_node(sender=self.sender, conn_node=self.successor(), sender_node=sender)

        if scrapper.valid_ref():
            self.scrapper_nodes.append(scrapper)

        return ret_scrapper_node(scrapper=scrapper)

    def ask_set_finger(self, params: str) -> Message:
        finger, pos = decode_post_finger(params)
        if belongs_to_interval(finger.id, self.id, self.finger_table[pos].id):
            self.finger_table[pos] = finger

            if not finger.same_ref(self.predecessor()):
                req_post_finger(sender=self.sender, conn_node=self.predecessor(), finger=finger, pos=pos)
            print(str(pos) + ' finger changed')
        return ret_post_finger()

    def get_pred_key(self, key: str) -> Message:
        pred_node = self.find_predecessor(int(key))
        print('Predecessor of key ' + str(key) + ' found: ' + str(pred_node.id))
        return ret_pred_of_key(pred_node)

    def get_pred_node(self) -> Message:
        print('Predecessor node found: ' + str(self.predecessor().id))
        return ret_pred_of_node(self.predecessor())

    def set_finger(self, params: str) -> Message:
        finger, pos = decode_post_finger(params)
        self.finger_table[pos] = finger
        print(str(pos) + ' finger changed')
        return ret_set_finger()

    def get_succ_key(self, key: str) -> Message:
        succ_node = self.find_successor(int(key))
        print('Succesor of key ' + str(key) + ' found: ' + str(succ_node.id))
        return ret_succ_of_key(succ_node)

    def get_succ_node(self) -> Message:
        print('Successor node found: ' + str(self.successor().id))
        return ret_succ_of_node(self.successor())

    def ask_add_scrap_node(self, scrapper_node: str):
        scrap_node = NodeReference()
        scrap_node.unpack(text=scrapper_node)

        assert scrap_node.valid_ref(), 'Invalid scrapper node received'

        self.scrapper_nodes.append(scrap_node)

    def notify_predecessor(self, node: str):
        pred_node = Finger()
        pred_node.unpack(text=node)

        if belongs_to_interval(pred_node.id, self.id, self.successor().id):
            self.finger_table[1] = pred_node

        return ret_post_pred()

    def set_url_info(self, url_pack: str):
        url, url_info = decode_url_info(url_pack=url_pack)
        url_hash = get_hash(text=url)

        if belongs_to_interval(url_hash, self.predecessor().id, self.id):
            self.dict_url[url_hash] = url_info
        else:
            successor = self.find_successor(id=url_hash)
            req_set_url(sender=self.sender, conn_node=successor, url=url, url_info=url_info)

