import os
import argparse
import socket
import logging

DEFAULT_IP = '127.0.0.1'
DEFAULT_PORT = 9999

def get_arguments():
    """Setup and parse arguments."""
    parser = argparse.ArgumentParser(description='P2P Client')
    parser.add_argument('-i', '--ip', type=str, required=False, default=DEFAULT_IP)
    parser.add_argument('-p', '--port', type=int, required=False, default=DEFAULT_PORT)

    return parser.parse_args()


def message_to_address(data):
    ip, port = data.decode('utf-8').strip().split(':')
    return (ip, int(port))


def main():
    """Entry point module."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[logging.StreamHandler(os.sys.stdout)]
    )

    args = get_arguments()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(b'HANDSHAKE', (args.ip, args.port))

    error_buf = None
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            message = data.decode('utf-8')
            logging.info(f'Client received data {message} from {addr}')
            addr = message_to_address(data)
            sock.sendto(b'HANDSHAKE', addr)
            data, addr = sock.recvfrom(1024)
            message = data.decode('utf-8')
            logging.info(f'Client received data {message} from {addr}')
        except Exception as error:
            message = f'Client crash: {error} {error.with_traceback}'
            if error_buf != message:
                error_buf = message
                logging.error(message)


if __name__ == '__main__':
    main()