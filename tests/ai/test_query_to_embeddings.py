from ai.query_data_to_embedding import query_to_embeddings

def test_uses_cache_on_hit():
    class EmbeddingServiceStub:
        def __init__(self):
            self.called = False

        def get_embeddings(self):
            raise "should not be called"
        
    class EmbeddingCacheStub:
        # def exists?
        # def fetch -> <embedding>
        # def sha -> <string> put in the sha capabilities

        def __init__(self):
            self.called = False

        def exists(self):
            raise "should not be called"
        
        def fetch():
            None

        def sha():
            None

    expected_embedding = ""
    embedding_service_stub = EmbeddingServiceStub()
    embedding_cache_stub = EmbeddingCacheStub()
    query_texts = []
    embeddings = query_to_embeddings(embedding_cache_stub, embedding_service_stub, query_texts)

    assert len(embeddings) > 0
    assert embeddings[0] == expected_embedding
    assert embedding_service_stub.called == False

def test_uses_ai_service_on_miss():
    None
