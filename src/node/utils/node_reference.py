class NodeReference:
    def __init__(self, ip='', port=''):
        self.ip = ip
        self.port = port

    def pack(self):
        return self.ip + '%' + self.port

    def unpack(self, text: str):
        self.ip, self.port = text.split('%')

    def same_ref(self, node_ref):
        return self.ip == node_ref.ip and self.port == node_ref.port

    def valid_ref(self):
        return (not self.ip == '') and (not self.port == '')


class Finger(NodeReference):
    def __init__(self, ip='', port='', finger_id=0):
        super().__init__(ip=ip, port=port)
        self.id: int = int(finger_id)

    def pack(self):
        return super().pack() + '%' + str(self.id)

    def unpack(self, text: str):
        args = text.split('%')
        assert len(args) == 3, 'Incorrect finger received'
        self.ip = args[0]
        self.port = args[1]
        self.id = int(args[2])
