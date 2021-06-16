m = 4

def get_hash(text: str):
    import hashlib

    h = hashlib.sha256(text.encode("utf-8"))
    n = int(h.hexdigest(), base=16)
    n = n % (2 ** m)
    return n

def belongs_to_interval(id, start_inter, end_inter):
    return (start_inter < id and id <= end_inter) or (start_inter >= end_inter and (start_inter < id or id <= end_inter))

def belongs_to_open_interval(id, start_inter, end_inter):
    return (start_inter < id and id < end_inter) or (start_inter >= end_inter and (start_inter < id or id < end_inter))

def finger_number(id, i):
    return (id + 2 ** (i - 1)) % (2 ** m)

def chord_number(id: int):
    return id % (2 ** m)