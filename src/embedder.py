from sentence_transformers import SentenceTransformer
import os

class Embedder:
    def __init__(self, model_path):
        if not os.path.isdir(model_path):
            raise FileNotFoundError(f"Model directory not found: {model_path}")
        self.model = SentenceTransformer(model_path)

    def embed(self, texts):
        """
        Embed a single string or a list of strings.
        """
        if isinstance(texts, str):
            texts = [texts]
        embeddings = self.model.encode(texts, convert_to_tensor=False, show_progress_bar=False)
        return embeddings if len(embeddings) > 1 else embeddings[0]
