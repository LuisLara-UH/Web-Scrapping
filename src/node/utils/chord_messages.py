from .sender import Sender
from .node_reference import NodeReference
from .message import *
from .codifiers import *


def req_succ_of_key(sender: Sender, conn_node: NodeReference, key: int):
    msg = Message(action=GET_SUCC_KEY, parameters=code_key(key))
    ret_msg = sender.request(conn_node, msg=msg)

    assert ret_msg.action == RET_SUCC_KEY, "Incorrect reply for successor key request"

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

    assert ret_msg.action == RET_SUCC_NODE, "Incorrect reply for successor node request"

    successor = decode_finger(ret_msg.parameters)
    print('Successor returned from msg:', successor.id)
    return successor


def ret_succ_of_node(node: Finger):
    return Message(action=RET_SUCC_NODE, parameters=code_finger(node))


def get_pred_of_node(sender: Sender, conn_node: NodeReference):
    msg = Message(action=GET_PRED_NODE)
    print('get pred 1')
    ret_msg = sender.request(conn_node=conn_node, msg=msg)
    print('get pred 2')

    assert ret_msg.action == RET_PRED_NODE, "Incorrect reply for successor node request"

    successor = decode_finger(ret_msg.parameters)

    print('return successor')
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


def req_scrapper_node(sender: Sender, conn_node: NodeReference, sender_node: NodeReference) -> NodeReference:
    msg = Message(action=GET_SCRAP_NODE, parameters=sender_node.pack())
    ret_msg = sender.request(conn_node=conn_node, msg=msg)

    assert ret_msg.action == RET_SCRAP_NODE, 'Incorrect reply for get scrapper node'

    scrapper = NodeReference()
    scrapper.unpack(ret_msg.parameters)

    return scrapper


def ret_scrapper_node(scrapper: NodeReference) -> Message:
    print('ret scrapper node pack')
    return Message(action=RET_SCRAP_NODE, parameters=scrapper.pack())


def ret_post_scrap_node() -> Message:
    return Message(action=RET_POST_SCRAP_NODE)


def req_scrap_url(sender: Sender, conn_node: NodeReference, url: str):
    msg = Message(action=GET_SCRAP_URL, parameters=url)
    ret_msg = sender.request(conn_node=conn_node, msg=msg, wait_time=-1)

    assert ret_msg.action == RET_SCRAP_URL, 'Incorrect reply for get scrapper url'
    assert not ret_msg.parameters == '', 'Invalid url info'

    return ret_msg.parameters


def req_chord_url(sender: Sender, conn_node: NodeReference, url: str):
    req_msg = Message(action=GET_CHORD_URL, parameters=url)
    ret_msg = sender.request(conn_node=conn_node, msg=req_msg)

    assert ret_msg.action == RET_CHORD_URL, "Incorrect answer to get url from chord node"
    
    assert not ret_msg.parameters == '', "Incorrect parameters in answer to get url from chord node"

    return ret_msg.parameters


def req_post_pred(sender: Sender, conn_node: NodeReference, pred_node: Finger):
    req_msg = Message(action=GET_POST_PRED, parameters=pred_node.pack())
    ret_msg = sender.request(conn_node=conn_node, msg=req_msg)

    assert ret_msg.action == RET_POST_PRED, 'Incorrect reply to notify predecessor'


def ret_post_pred() -> Message:
    return Message(action=RET_POST_PRED)


def req_set_url(sender: Sender, conn_node: NodeReference, url: str, url_info: str):
    url_pack = code_url_info(url=url, url_info=url_info)
    req_msg = Message(action=GET_SET_URL, parameters=url_pack)
    rep_msg = sender.request(conn_node=conn_node, msg=req_msg)

    assert rep_msg.action == RET_SET_URL, 'Incorrect reply to set url info'


def ret_set_url() -> Message:
    return Message(action=RET_SET_URL)


def req_check_node(sender: Sender, conn_node: NodeReference) -> Message:
    msg = Message(action=GET_CHECK_NODE)
    rep_msg = sender.request(conn_node=conn_node, msg=msg)

    return rep_msg


def ret_check_node() -> Message:
    return Message(action=RET_CHECK_NODE)
