import os
from langchain_openai import OpenAIEmbeddings
from common.logger import Logger
from common.paths import Paths
from common.models import OPENAI_EMBEDDING_MODEL

class EmbeddingService:
    def load_api_key(self, filename):
        with open(filename, 'r') as file:
            content = file.read()
        return content

    def fetch(self, data):
        model_name = OPENAI_EMBEDDING_MODEL
        secrets_dir = os.path.join(Paths.PROJECT_DIR, "secrets")
        api_key_file = os.path.join(secrets_dir, "api-key")
        api_key = self.load_api_key(api_key_file)

        embedding_api = OpenAIEmbeddings(
            model=model_name,
            api_key=api_key.strip(),
        )

        Logger.log(f"embedding service is embedding {len(data)} records")

        embeddings = embedding_api.embed_documents(data)
        return embeddings
