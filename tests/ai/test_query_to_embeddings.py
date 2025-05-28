from ai.query_data_to_embedding import query_to_embeddings

def test_uses_cache_on_hit():
    class EmbeddingServiceStub:
        def __init__(self):
            self.called = False

        def fetch(self, query_texts):
            raise "should not be called"
        
    class EmbeddingCacheStub:
        def __init__(self):
            self.set_called = False

        def contains(self, key):
            return True
        
        def get(self, key):
            return ["cached_embedding"]
        
        def set(self, name):
            raise "set should not be called"

        def sha(self):
            return "cached_embedding_sha"

    embedding_service_stub = EmbeddingServiceStub()
    embedding_cache_stub = EmbeddingCacheStub()
    query_texts = ["query_a"]
    embeddings = query_to_embeddings(embedding_cache_stub, embedding_service_stub, query_texts)

    assert len(embeddings) > 0
    assert embeddings[0] == ["cached_embedding"]

def test_uses_ai_service_on_miss():
    class EmbeddingServiceStub:
        def fetch(self, query_texts):
            return [['new_embedding']]
        
    class EmbeddingCacheStub:
        def __init__(self):
            self.set_called = False

        def contains(self, key):
            return False
        
        def get(self, key):
            raise "get should not be called"
        
        def set(self, name, value):
            self.set_called = True
        
    embedding_service_stub = EmbeddingServiceStub()
    embedding_cache_stub = EmbeddingCacheStub()
    query_texts = ["query_a"]
    embeddings = query_to_embeddings(embedding_cache_stub, embedding_service_stub, query_texts)

    assert len(embeddings) > 0
    assert embeddings[0] == ["new_embedding"]
    assert embedding_cache_stub.set_called == True
