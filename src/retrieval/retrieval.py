import sys

from langchain_core.output_parsers import StrOutputParser
from langchain_qdrant import QdrantVectorStore
from src.utils.model_loader import ModelLoader
from src.logger import GLOBAL_LOGGER as log 
from src.exception.custom_exception import CustomException
from src.utils.config_loader import load_config
from src.prompts.prompts import PROMT_REGISTRY

class ConversationalRAG:
    def __init__(self):
        # build retirvel
        #self.model_loader=ModelLoader()
        self.embed_model=ModelLoader().load_embedding()
        self.config=load_config()
        self.llm = self._load_llm()
        self.retrievar=self._load_qdrant_retrieval()
        
        # buld prompt
        self.chain=None
        if self.retrievar is not None:
            self.chain=self._build_lcel_chain()
            
            
    def _load_qdrant_retrievar(self):
        vectorstore=QdrantVectorStore.from_existing_collection(
            embedding=self.embed_model,
            path="qdrantdb",
            collection_name="document_chat"
        )
        topk = self.config["retriever"]["top_k"]
        retrievar=vectorstore.as_retriever(search_args={"k":topk})
        return retrievar
        
    def _load_llm(self):
        try:
            llm=ModelLoader().load_llm()
            if not llm:
                raise ValueError("LLM could not be found")
            log.info("LLM loaded successfully")
            return llm
        except Exception as e:
            log.error("failed top load LLM",error=str(e))  
            raise CustomException("LLM loading faild in ConersationalRAG",sys)
        
    def _build_lcel_chain(self,payload):
        try:
            # 1. Rewrite user question with chathistory contecxt
            context_question_prompt=PROMT_REGISTRY["contextualize_question"]
            question_rewriter=(
                {"input":payload.input,"chat_history":payload.chat_history}
                | context_question_prompt
                | self.llm
                | StrOutputParser
            )
            
            retrievedocs= question_rewriter | self.retrievar | self._format_docs
            
            # 2. Anserr using retrieved context + question rewriter
            context_qa_prompt=PROMT_REGISTRY["context_qa"]
            self.chain=(
                {"context":retrievedocs,"input":payload.input}
                | context_qa_prompt
                | self.llm
                | StrOutputParser
            )
              
            log.info("LCEL graph build successfully]")  
        except Exception as e:
            log.error("failed to build LCEL chain in ConverstaionalRAG",error=str(e))
            raise CustomException("failed to build LCEL chain in ConverstaionalRAG")
        
    def _format_docs(self,docs):
         context = " ".join([doc.page_content for doc in docs])
         return context
         
    def invoke(self,user_input,chat_history):
        try:
            if self.chain is None:
                raise CustomException("Rag chain not initialized",sys)
            
            chat_history=chat_history or []
            payload={"input":user_input,"chat_history":chat_history}
            answer=self.chain.invoke(payload)
            if not answer:
                log.warning("No answer generated",user_input=user_input)
                return "no answer generated"
            
            log.info("chain invoked successfullya nd generated answer",user_input=user_input,answer=str(answer["100"]))
            return answer   
        except Exception as e:
            log.error("failed to invoke ConversationalRAG",error=str(e))
            raise CustomException("ailed to invoke ConversationalRAG",sys)
        
    