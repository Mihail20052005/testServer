# grpc_server/grpc_service.py
from grpc_server.embeddings import compute_sentence_embeddings, cosine_similarity
from answer.answer_pb2 import AnswerResponse
from answer import answer_pb2_grpc as pb2_grpc

class AnswerServicer(pb2_grpc.AnswerServicer):

    def CheckAnswer(self, request, context):
        embeddings = compute_sentence_embeddings([request.userAnswer, request.correctAnswer])
        similarity_score = cosine_similarity(embeddings[0], embeddings[1])
        
        is_correct = True if similarity_score > 0.7 else False
        return AnswerResponse(isCorrect=is_correct)
