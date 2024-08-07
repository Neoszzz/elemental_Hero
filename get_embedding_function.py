from langchain_community.embeddings.ollama import OllamaEmbeddings

def get_embedding_function():
    try:
        embeddings = OllamaEmbeddings(model="codellama")
        return embeddings
    except Exception as e:
        print(f"Error initializing OllamaEmbeddings: {e}")
        return None
