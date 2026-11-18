"""
backend/app/routers/chat.py
Router for CareerFit AI Assistant Chatbot (Milestone 2 - Points 16 & 17)
"""

from fastapi import APIRouter, HTTPException
from backend.app.models.schemas import (
    ChatMessageRequest,
    ChatMessageResponse
)
from backend.app.services.chatbot_service import handle_chat_query

router = APIRouter(prefix="/chat", tags=["AI Assistant"])

@router.post("/message", response_model=ChatMessageResponse)
def send_chat_message(req: ChatMessageRequest):
    """
    Universal Chat API endpoint for interactive AI career guidance.
    """
    try:
        return handle_chat_query(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process message: {str(e)}")
