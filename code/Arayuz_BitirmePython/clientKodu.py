import socket
import time

def send_command(host='127.0.0.1', port=5000, command="TEST"):
    """TCP ile komut gönderen fonksiyon"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3)  # 3 saniye timeout
            s.connect((host, port))
            s.sendall(command.encode('utf-8'))
            response = s.recv(1024).decode('utf-8')
            print(f"Sunucu yanıtı: {response}")
            return True
    except Exception as e:
        print(f"Bağlantı hatası: {e}")
        return False

if __name__ == "__main__":
    commands = ["sag","bekle", "sol", "dur","ileri","engel","geri","xyx"]
    
    while True:
        for cmd in commands:
            print(f"{cmd} komutu gönderiliyor...")
            send_command(command=cmd)
            time.sleep(2)  # 2 saniyede bir komut gönder