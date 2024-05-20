import grpc
from concurrent import futures
import model_pb2 as pb2
import model_pb2_grpc as pb2_grpc
from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("ai-forever/sbert_large_nlu_ru")
model = AutoModel.from_pretrained("ai-forever/sbert_large_nlu_ru")

# Mean Pooling
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    return sum_embeddings / sum_mask

# Compute sentence embeddings
def compute_sentence_embeddings(sentences):
    encoded_input = tokenizer(sentences, padding=True, truncation=True, max_length=24, return_tensors='pt')
    with torch.no_grad():
        model_output = model(**encoded_input)
    sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])
    return sentence_embeddings

# Calculate cosine similarity
def cosine_similarity(embedding1, embedding2):
    return F.cosine_similarity(embedding1.unsqueeze(0), embedding2.unsqueeze(0)).item()

class YourModelServicer(pb2_grpc.YourModelServicer):
    def ComputeSimilarity(self, request, context):
        embeddings = compute_sentence_embeddings([request.sentence1, request.sentence2])
        similarity_score = cosine_similarity(embeddings[0], embeddings[1])
        return pb2.SimilarityResponse(score=similarity_score)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_YourModelServicer_to_server(YourModelServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    while(True):
        serve()
