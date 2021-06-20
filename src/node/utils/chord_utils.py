m = 4


def get_hash(text: str):
    import hashlib

    h = hashlib.sha256(text.encode("utf-8"))
    n = int(h.hexdigest(), base=16)
    n = n % (2 ** m)
    return n


def belongs_to_interval(finger_id, start_inter, end_inter):
    return (start_inter < finger_id <= end_inter) or \
           (start_inter >= end_inter and (start_inter < finger_id or finger_id <= end_inter))


def belongs_to_open_interval(finger_id, start_inter, end_inter):
    return (start_inter < finger_id < end_inter) or \
           (start_inter >= end_inter and (start_inter < finger_id or finger_id < end_inter))


def finger_number(finger_id, i):
    return (finger_id + 2 ** (i - 1)) % (2 ** m)


def chord_number(finger_id: int):
    return finger_id % (2 ** m)
