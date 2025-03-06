from services.chat_service import ChatService
from core.vector_store import VectorStore
from core.rag_system import RAGSystem
from typing import List
from model.chat_message import ChatMessage
from model.chat_session import ChatSession
from config.config import Config


class ChatController(ChatService):

    def __init__(self):
        
        try:
            self.vector_db = VectorStore(collection_name=Config.EMBEDDING_COLLECTION_NAME)
            self.rag_system = RAGSystem(self.vector_db)

        except Exception as e: 
             print(f"Error Initializing the RAG System: {e}")
           


    async def chat_with_bot(self, session_id:str, user_id:str, question:str):
        try: 

            async for chunk in self.rag_system.query_as_stream(
                session_id=session_id,
                user_id=user_id,
                question=question, 
            ):
                yield chunk
            
            self.vector_db.store_session_metadata(session_id=session_id, user_id=user_id, question=question)

        except Exception as e: 
            print(f"Error: {e}")
            yield f"{e}!"

    async def get_chat_history(self, session_id:str, user_id:str) -> List[ChatMessage]:
        try: 
           return  self.vector_db.get_chat_history(user_id=user_id, session_id=session_id)
        except Exception as e: 
            print(f"Error: {e}")
            return []


    async def delete_chat_history(self, session_id:str, user_id:str) -> bool: 
        try: 
            self.vector_db.delete_chat_history(user_id=user_id, session_id=session_id)
            return True
        
        except Exception as e: 
            print(f"Error: {e}")
            return False

    async def rename_chat_session(self, session_id: str, user_id: str, new_name:str)-> bool:
        try: 
            self.vector_db.rename_session(user_id=user_id, session_id=session_id, new_name=new_name)
            return True
        
        except Exception as e: 
            print(f"Error: {e}")
            return False


    async def get_chat_session_list(self, user_id: str) -> List[ChatSession]:
        
        try: 
           return self.vector_db.get_session_list(user_id=user_id)
        
        except Exception as e: 
            print(f"Error: {e}")
            return []







    