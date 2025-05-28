import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from common.logger import Logger
from common.paths import Paths

class EmbeddingService:
    def load_api_key(self, filename):
        with open(filename, 'r') as file:
            content = file.read()
        return content

    def fetch(self, data):
        model_name = "models/text-embedding-004"
        secrets_dir = os.path.join(Paths.PROJECT_DIR, "secrets")
        api_key_file = os.path.join(secrets_dir, "google-api-key")
        api_key = self.load_api_key(api_key_file)

        embedding_api = GoogleGenerativeAIEmbeddings(
            model=model_name,
            google_api_key = api_key
        )

        Logger.log(f"embedding service is embedding {len(data)} records")

        embeddings = embedding_api.embed_documents(data)
        return embeddings