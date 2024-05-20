import grpc
import model_pb2
import model_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = model_pb2_grpc.YourModelStub(channel)
    while True:
        sentence1 = input("Enter the first sentence (or type 'exit' to quit): ")
        if sentence1.lower() == 'exit':
            break
        sentence2 = input("Enter the second sentence: ")
        response = stub.ComputeSimilarity(model_pb2.SimilarityRequest(sentence1=sentence1, sentence2=sentence2))
        print("Similarity score:", response.score)

if __name__ == '__main__':
    run()
