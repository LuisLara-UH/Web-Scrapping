from abc import abstractstaticmethod
from .sender import Sender
from .node_reference import NodeReference
from .message import *
from .codifiers import *

def req_succ_of_key(sender: Sender, conn_node: NodeReference, key: int):
    msg = Message(action=GET_SUCC_KEY, parameters=code_key(key))
    ret_msg = sender.request(conn_node, msg=msg)

    assert ret_msg.action == RET_SUCC_KEY, "Incorrect reply for succesor key request"

    successor = decode_finger(ret_msg.parameters)

    return successor

def ret_succ_of_key(node: Finger):
    return Message(action=RET_SUCC_KEY, parameters=code_finger(node))

def req_pred_of_key(sender: Sender, conn_node: NodeReference, key: int):
    msg = Message(action=GET_PRED_KEY, parameters=code_key(key))
    ret_msg = sender.request(conn_node, msg=msg)

    assert ret_msg.action == RET_PRED_KEY, "Incorrect reply for predecessor node request"

    predecessor = decode_finger(ret_msg.parameters)

    return predecessor

def ret_pred_of_key(node: Finger):
    return Message(action=RET_PRED_KEY, parameters=code_finger(node))

def get_succ_of_node(sender: Sender, conn_node: NodeReference):
    msg = Message(action=GET_SUCC_NODE)
    ret_msg = sender.request(conn_node, msg=msg)

    assert ret_msg.action == RET_SUCC_NODE, "Incorrect reply for succesor node request"

    successor = decode_finger(ret_msg.parameters)

    return successor

def ret_succ_of_node(node: Finger):
    return Message(action=RET_SUCC_NODE, parameters=code_finger(node))

def get_pred_of_node(sender: Sender, conn_node: NodeReference):
    msg = Message(action=GET_PRED_NODE)
    ret_msg = sender.request(conn_node, msg=msg)

    assert ret_msg.action == RET_PRED_NODE, "Incorrect reply for succesor node request"

    successor = decode_finger(ret_msg.parameters)

    return successor

def ret_pred_of_node(node: Finger):
    return Message(action=RET_PRED_NODE, parameters=code_finger(node))

def req_set_finger(sender: Sender, conn_node: NodeReference, finger: Finger, pos: int):
    msg = Message(action=GET_SET_FINGER, parameters=code_post_finger(finger=finger, pos=pos))
    ret_msg = sender.request(conn_node=conn_node, msg=msg)

    assert ret_msg.action == RET_SET_FINGER, "Incorrect reply for set finger"

def ret_set_finger():
    return Message(action=RET_SET_FINGER)

def req_post_finger(sender: Sender, conn_node: NodeReference, finger: Finger, pos: int):
    msg = Message(action=GET_POST_FINGER, parameters=code_post_finger(finger=finger, pos=pos))
    ret_msg = sender.request(conn_node=conn_node, msg=msg)

    assert ret_msg.action == RET_POST_FINGER, "Incorrect reply for post finger"

def ret_post_finger():
    return Message(action=RET_POST_FINGER)

def ret_url_info(url_info: str):
    return Message(action=RET_CHORD_URL, parameters=url_info)