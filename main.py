# main.py
from grpc_server.server import Server
import logging

def main():
    logging.basicConfig(level=logging.INFO)
    server = Server(addr="[::]:50051")
    server.serve()
    

if __name__ == "__main__":
    main()
    