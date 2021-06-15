from .node_reference import Finger

def code_finger(finger: Finger):
    return finger.ip + '%' + finger.port + '%' + finger.id

def decode_finger(text: str):
    props = text.split('%')
    assert len(props) == 3, 'Incorrect finger received'

    return Finger(ip=props[0], port=props[1], id=props[2])

def code_key(key: int):
    return str(key)

def decode_key(key: str):
    return int(key)

def code_post_finger(finger: Finger, pos: int):
    return code_finger(finger=finger) + '%' + str(pos)

def decode_post_finger(post_finger: str):
    props = post_finger.split('%')
    assert len(props) == 4, "Incorrect post finger request received"

    return Finger(ip=props[0], port=props[1], id=props[2]), int(props[3]) 