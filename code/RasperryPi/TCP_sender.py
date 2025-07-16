import socket


def TCP_sender(command):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('10.255.36.83', 5000))
        s.send(command.encode('utf-8'))
        s.close()
    except Exception as e:
        print("Gönderim hatası:", e)


