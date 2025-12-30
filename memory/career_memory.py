import faiss
import numpy as np
import pickle
import os

class CareerMemory:
    def __init__(self, index_file="career_memory.index"):
        self.index_file = index_file
        self.dimension = 384 # Example dimension for embeddings
        self.index = faiss.IndexFlatL2(self.dimension)
        self.metadata = []
        if os.path.exists(index_file):
            self.load()

    def add_memory(self, embedding, meta):
        """
        Add an embedding and its metadata to the memory.
        embedding: numpy array of shape (dimension,)
        meta: dict containing metadata
        """
        if len(embedding) != self.dimension:
            raise ValueError(f"Embedding dimension must be {self.dimension}")
        
        # Reshape for FAISS
        vector = np.array([embedding]).astype('float32')
        self.index.add(vector)
        self.metadata.append(meta)
        self.save()

    def search_memory(self, query_embedding, k=5):
        """
        Search for the k nearest neighbors.
        """
        vector = np.array([query_embedding]).astype('float32')
        distances, indices = self.index.search(vector, k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx < len(self.metadata):
                results.append({
                    "metadata": self.metadata[idx],
                    "distance": distances[0][i]
                })
        return results

    def save(self):
        faiss.write_index(self.index, self.index_file)
        with open(self.index_file + ".meta", "wb") as f:
            pickle.dump(self.metadata, f)

    def load(self):
        self.index = faiss.read_index(self.index_file)
        with open(self.index_file + ".meta", "rb") as f:
            self.metadata = pickle.load(f)
