# grpc_server/server.py
import grpc
from concurrent import futures                                                            
import time
import logging

import grpc._interceptor
from grpc_server.grpc_service import AnswerServicer
from answer.answer_pb2_grpc import add_AnswerServicer_to_server

class Server:
    def __init__(self, addr: str) -> None:
        self.addr = addr

    def serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        add_AnswerServicer_to_server(AnswerServicer(), server)
        server.add_insecure_port(address=self.addr)
        server.start()
        logging.info('server starting on %s', self.addr)
        server.wait_for_termination()
