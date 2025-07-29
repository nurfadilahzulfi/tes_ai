import json
import os
from datetime import datetime
from typing import List, Dict, Any
import logging

def format_chat_message(role: str, content: str, timestamp: str = None) -> Dict[str, str]:
    """
    Format chat message with proper structure
    
    Args:
        role: 'user' or 'assistant'
        content: Message content
        timestamp: Optional timestamp
        
    Returns:
        Formatted message dictionary
    """
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return {
        "role": role,
        "content": content,
        "timestamp": timestamp
    }

def save_chat_history(messages: List[Dict[str, Any]], filename: str = None) -> bool:
    """
    Save chat history to JSON file
    
    Args:
        messages: List of chat messages
        filename: Optional custom filename
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Create logs directory if it doesn't exist
        os.makedirs("logs", exist_ok=True)
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"logs/chat_history_{timestamp}.json"
        
        chat_data = {
            "timestamp": datetime.now().isoformat(),
            "total_messages": len(messages),
            "messages": messages
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(chat_data, f, ensure_ascii=False, indent=2)
        
        logging.info(f"Chat history saved to {filename}")
        return True
        
    except Exception as e:
        logging.error(f"Failed to save chat history: {e}")
        return False

def load_chat_history(filename: str) -> List[Dict[str, Any]]:
    """
    Load chat history from JSON file
    
    Args:
        filename: Path to chat history file
        
    Returns:
        List of chat messages or empty list if failed
    """
    try:
        if not os.path.exists(filename):
            return []
        
        with open(filename, 'r', encoding='utf-8') as f:
            chat_data = json.load(f)
        
        messages = chat_data.get("messages", [])
        logging.info(f"Loaded {len(messages)} messages from {filename}")
        return messages
        
    except Exception as e:
        logging.error(f"Failed to load chat history: {e}")
        return []

def validate_input(text: str, max_length: int = 2000) -> Dict[str, Any]:
    """
    Validate user input
    
    Args:
        text: Input text to validate
        max_length: Maximum allowed length
        
    Returns:
        Dictionary with validation result
    """
    result = {"valid": True, "errors": []}
    
    if not text or not text.strip():
        result["valid"] = False
        result["errors"].append("Input tidak boleh kosong")
    
    if len(text) > max_length:
        result["valid"] = False
        result["errors"].append(f"Input terlalu panjang (maksimal {max_length} karakter)")
    
    # Check for potentially harmful content
    harmful_patterns = ["<script", "javascript:", "eval(", "exec("]
    for pattern in harmful_patterns:
        if pattern.lower() in text.lower():
            result["valid"] = False
            result["errors"].append("Input mengandung konten yang tidak diizinkan")
            break
    
    return result

def clean_response(text: str) -> str:
    """
    Clean and format AI response
    
    Args:
        text: Raw response text
        
    Returns:
        Cleaned response text
    """
    if not text:
        return ""
    
    # Remove excessive whitespace
    text = " ".join(text.split())
    
    # Remove potential harmful content
    text = text.replace("<script", "&lt;script")
    text = text.replace("</script>", "&lt;/script&gt;")
    
    return text

def get_file_size(filepath: str) -> str:
    """
    Get human-readable file size
    
    Args:
        filepath: Path to file
        
    Returns:
        File size as string (e.g., "1.5 MB")
    """
    try:
        size_bytes = os.path.getsize(filepath)
        
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024**2:
            return f"{size_bytes/1024:.1f} KB"
        elif size_bytes < 1024**3:
            return f"{size_bytes/(1024**2):.1f} MB"
        else:
            return f"{size_bytes/(1024**3):.1f} GB"
            
    except Exception:
        return "Unknown"

def setup_logging(log_level: str = "INFO", log_file: str = None):
    """
    Setup logging configuration
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional log file path
    """
    try:
        # Create logs directory
        if log_file:
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        # Setup logging format
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        # Configure logging
        handlers = [logging.StreamHandler()]
        if log_file:
            handlers.append(logging.FileHandler(log_file, encoding='utf-8'))
        
        logging.basicConfig(
            level=getattr(logging, log_level.upper()),
            format=log_format,
            handlers=handlers
        )
        
        logging.info("Logging configured successfully")
        
    except Exception as e:
        print(f"Failed to configure logging: {e}")

def format_timestamp(timestamp: str = None) -> str:
    """
    Format timestamp for display
    
    Args:
        timestamp: ISO timestamp string or None for current time
        
    Returns:
        Formatted timestamp string
    """
    try:
        if timestamp:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        else:
            dt = datetime.now()
        
        return dt.strftime("%d/%m/%Y %H:%M:%S")
        
    except Exception:
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")