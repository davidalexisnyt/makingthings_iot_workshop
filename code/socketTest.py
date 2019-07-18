import socket

address_info = socket.getaddrinfo("towel.blinkenlights.nl", 23)
address = address_info[0][-1]
s = socket.socket()
s.connect(address)

while True:
    data = s.recv(500)
    print(str(data, 'utf-8'), end='')
