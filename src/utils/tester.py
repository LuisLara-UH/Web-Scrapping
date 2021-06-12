from message import Message

def test_message():
    actions = ['get', 'get-chord', 'ret-chord']
    parameters = ['23%89', '1%4%ip', '127.0.0.1%8888']

    for i in range(len(actions)):
        msg = Message(action=actions[i], parameters=parameters[i])
        assert msg.action == actions[i], "Action not set correctly"
        assert msg.parameters == parameters[i], "Parameters not set correctly"

        msg_pack = msg.pack()
        assert msg_pack == actions[i] + '%' + parameters[i], "Message not packed correctly"

        msg.unpack(actions[i] + '%' + parameters[i])
        assert msg.action == actions[i], "Action not unpacked correctly"
        assert msg.parameters == parameters[i], "Parameters not unpacked correctly"


print('Testing message...')
test_message()

print('Testing succesful')