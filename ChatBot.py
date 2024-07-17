from typing import Protocol
from ChatBotUtils.privateInfo import OPENAI_API_KEY
from openai import OpenAI
import base64
# import for database embedding
from llama_index.core.node_parser import  SimpleNodeParser
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.core import load_index_from_storage
from llama_index.core import (
    Settings,
    Document,
    VectorStoreIndex,
    StorageContext
)
from chromadb import PersistentClient
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.storage.index_store import SimpleIndexStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.core.indices.vector_store.retrievers.retriever import VectorIndexRetriever
import json 
from FixedContent import FixedContent


# API key for OpenAI
client = OpenAI(
    api_key = OPENAI_API_KEY,
)
# Set embedding model
Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en"
)

def build_database():
    # Open json file
    with open('ChatBotUtils/database_content.json', encoding='utf-8') as json_data:
        data = json.load(json_data)
        json_data.close()

    # Document data into database
    docs=[]
    for idx,(func_name,desc) in enumerate(data.items()):
        docs.append(Document(
            text=desc['description'],
            doc_id=idx,
            extra_info={
                'content': json.dumps(desc['content']),
                'image_path': json.dumps(desc['image_path']),
            },
            excluded_llm_metadata_keys=["Pattern Template"],
            excluded_embed_metadata_keys=['content','image_path'],
        ))
    nodes = SimpleNodeParser().get_nodes_from_documents(docs)

    # Init database
    chroma_client = PersistentClient('ChatBotUtils/database/Doc')
    chroma_collection = chroma_client.get_or_create_collection("VisualizaionDatabase")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(docstore=SimpleDocumentStore(),vector_store=vector_store)
    storage_context.docstore.add_documents(nodes)
    index = VectorStoreIndex.from_documents(
        docs, storage_context=storage_context
    )
    index.storage_context.persist('ChatBotUtils/database/Doc')

def retrieve_database(content):
    # Load index from storage
    chroma_client = PersistentClient('ChatBotUtils/database/Doc')
    chroma_collection = chroma_client.get_or_create_collection("VisualizaionDatabase")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    storage_context = StorageContext.from_defaults(
            docstore=SimpleDocumentStore.from_persist_dir(persist_dir='ChatBotUtils/database/Doc'),
            vector_store=vector_store,
            index_store=SimpleIndexStore.from_persist_dir(persist_dir='ChatBotUtils/database/Doc')
    )
    bm25_retriever = BM25Retriever.from_defaults(docstore=storage_context.docstore, similarity_top_k=1)
    bm25_nodes = bm25_retriever.retrieve(content)
    for node in bm25_nodes:
        metadata = node.node.metadata
        content = metadata['content'].replace('"','')
        image_path = metadata['image_path'].replace('"','')
    print(image_path)
    return content, image_path


class OpenAIChatbot:
    # Function to encode the image to base64 encoded format
    def __encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
        
    # Fucntion to send prompt with an image
    def prompt_with_image(self, input_prompt, image_path):
        b64image = self.__encode_image(image_path)
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system", 
                    "content": "Bạn là một trợ lý phân tích dữ liệu. Đối tượng được phân tích là các sản phẩm hoặc các đánh giá sản phẩm trên một trang web thương mại điện tử. Bạn cần phân tích dữ liệu và đưa ra những kết luận hợp lý từ dữ liệu đã phân tích."
                },
                {
                    "role": "user", 
                    "content": [
                        {"type": "text", "text": input_prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64image}"}}
                    ]
                }
            ]
        )
        print(completion.choices[0].message)
        return completion.choices[0].message.content
    
    # Fucntion to send prompt with an image
    def prompt_without_image(self, input_prompt, content):
        prompt_content = f"""Từ câu hỏi của người dùng, hãy tiến hành phân tích và đưa ra kết luận từ thông tin được tôi cung cấp như sau:
        
        ### Câu hỏi của người dùng:
        {input_prompt}
        
        ### Thông tin được cung cấp:
        {content}
        """
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system", 
                    "content": "Bạn là một trợ lý phân tích dữ liệu. Đối tượng được phân tích là các sản phẩm hoặc các đánh giá sản phẩm trên một trang web thương mại điện tử. Bạn cần phân tích dữ liệu và đưa ra những kết luận hợp lý từ dữ liệu đã phân tích."
                },
                {
                    "role": "user", 
                    "content": [
                        {"type": "text", "text": prompt_content},
                    ]
                }
            ]
        )
        print(completion.choices[0].message)
        return completion.choices[0].message.content

    # Response to UI
    def generate_response(self, app_context) -> str:
        # Retrieve content from database
        prompt_retrieve = f"""{app_context.titlePage}: {app_context.prompt}"""
        answer = """"""
        content_id, image_path = retrieve_database(prompt_retrieve)

        # Send prompt with image in case image_path is available
        if image_path == 'None':
            fixedContent = FixedContent.get_instance()
            content_text = getattr(fixedContent, content_id)
            answer = self.prompt_without_image(app_context.prompt, content_text)
        
        # Send prompt with content only in case image_path is not available
        else: 
            answer = self.prompt_with_image(app_context.prompt, image_path)
        response = (f"{answer}")
        return response