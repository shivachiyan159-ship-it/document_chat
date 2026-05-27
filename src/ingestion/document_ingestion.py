from src.utils.file_ops import save_upload_files,load_documents
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.logger import GLOBAL_LOGGER as log
from src.utils.model_loader import ModelLoader
from src.utils.config_loader import load_config
from langchain_qdrant import QdrantVectorStore
from src.exception.custom_exception import CustomException

class DocumentIngestion():
    def __init__(self):
        self.model_loader=ModelLoader()
        self.config=load_config()

    def _splitchunks(self,docs,chunksize=1000,chunkoverlap=200):
        try:
            splitter=RecursiveCharacterTextSplitter(chunk_size=chunksize,chunk_overlap=chunkoverlap)
            chunks=splitter.split_documents(docs)
            log.info("Document split completed")
            return chunks
        except Exception as e:
            log.error("failed chunking")
            raise CustomException("error conerting chunks",e)
        
    def _storevectordb(self,chunks) -> QdrantVectorStore:
        try:
            embed_model=self.model_loader.load_embedding()
            vectorstore=QdrantVectorStore.from_documents(
                documents=chunks,
                embedding=embed_model,
                path="qdrantdb",
                collection_name="document_chat"
            )
            return vectorstore
        except Exception as e:
            log.error("failed storing vectordb",error=str(e))
            raise CustomException("error storing data into vectordb",e)
            
        
    def insertvectordb(self,uploadfiles,targetpath,chunksize,chunkoverlap):
        try:
            # load cocuments
            paths=save_upload_files(uploadfiles,targetpath)
            docs=load_documents(paths)
            # split chunks
            chunks=self._splitchunks(docs,chunksize,chunkoverlap)
            # convert embeddings and store into vectordb
            self._storevectordb(chunks)
            
            # topk=self.config["retriever"]["top_k"]
            # # return Rertriever
            # return vectorstore.as_retriever(search_args={"k":topk})
        except Exception as e:
            log.error("failed storing vectordb",error=str(e))
            raise CustomException("Error storing vectordb",e)
