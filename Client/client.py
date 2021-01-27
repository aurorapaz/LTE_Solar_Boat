import socket

SERVER_IP = 'solarboat.ddns.net'
SERVER_PORT = 12345
MESSAGE = b'Hello Server!'
BUFFER_SIZE = 1024

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP,SERVER_PORT))
    print('Sending data: ')
 
    f = open("myfile.txt", "rb")
    content = f.read(BUFFER_SIZE)
    
    while content:
        client.send(content)
        content = f.read(BUFFER_SIZE)
    
    print('File sent')

    data = client.recv(BUFFER_SIZE)

    client.close()
    f.close()

    print('The server responded: {}'.format(data))

        

if __name__ == '__main__':
    main()
