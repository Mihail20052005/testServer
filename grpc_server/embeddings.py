# grpc_server/embeddings.py
import torch
from transformers import AutoTokenizer, AutoModel
import torch.nn.functional as F
import logging

tokenizer = AutoTokenizer.from_pretrained("ai-forever/sbert_large_nlu_ru")
model = AutoModel.from_pretrained("ai-forever/sbert_large_nlu_ru")

def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    return sum_embeddings / sum_mask

def compute_sentence_embeddings(sentences):
    encoded_input = tokenizer(sentences, padding=True, truncation=True, max_length=24, return_tensors='pt')
    with torch.no_grad():
        model_output = model(**encoded_input)
    sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])
    return sentence_embeddings

def cosine_similarity(embedding1, embedding2):
    similarity = F.cosine_similarity(embedding1.unsqueeze(0), embedding2.unsqueeze(0)).item()
    logging.info('similarity: %f', similarity)
    return similarity
