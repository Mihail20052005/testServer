# main.py
from grpc_server.server import Server
import asyncio
import logging

def main():
    logging.basicConfig(level=logging.INFO)
    server = Server(addr="[::]:50051")
    asyncio.run(server.serve())
    

if __name__ == "__main__":
    main()
    