import os
from typing import List

class Config:
    """Configuration settings for the chatbot application"""
    
    # Ollama Server Settings
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "3600"))
    
    # Default Model Settings
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "llama3.1:8b")
    AVAILABLE_MODELS = [
        "llama3.1:8b",
        "llama3.2:3b", 
        "llama3.2:1b",
        "phi3:mini",
        "qwen2:0.5b",
        "deepseek-coder:1.3b-instruct"
    ]
    
    # Streamlit App Settings
    APP_TITLE = "🤖 AI Chatbot dengan Ollama"
    APP_DESCRIPTION = "Chatbot AI menggunakan model lokal Ollama"
    
    # Chat Settings
    MAX_MESSAGE_LENGTH = int(os.getenv("MAX_MESSAGE_LENGTH", "2000"))
    MAX_CHAT_HISTORY = int(os.getenv("MAX_CHAT_HISTORY", "50"))
    
    # UI Settings
    SIDEBAR_WIDTH = 300
    CHAT_CONTAINER_HEIGHT = 400
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs/chat_history.log")
    
    # System Prompts
    SYSTEM_PROMPTS = {
        "default": "Anda adalah asisten AI yang membantu dan informatif.",
        "coding": "Anda adalah expert programmer yang membantu dengan coding dan debugging.",
        "academic": "Anda adalah tutor akademik yang menjelaskan konsep dengan detail.",
        "creative": "Anda adalah asisten kreatif yang membantu dengan ide dan brainstorming."
    }
    
    # Response Settings
    DEFAULT_TEMPERATURE = 0.7
    DEFAULT_TOP_P = 0.9
    DEFAULT_TOP_K = 40