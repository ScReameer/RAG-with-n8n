from sentence_transformers import SentenceTransformer
import torch
import numpy as np

device = "cuda:0" if torch.cuda.is_available() else "cpu"
model = None


def load_model() -> None:
    """
    Loads the SentenceTransformer model.
    """
    global model
    if model is None:
        print("Loading model...")
        model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2', device=device)
        print("Model loaded.")


def encode(texts: list[str]) -> torch.Tensor | np.ndarray:
    """
    Encodes a list of texts into embeddings.
    """
    if model is None:
        raise RuntimeError("Model is not loaded. Call load_model() first.")
    return model.encode(texts, device=device)
