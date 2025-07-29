import requests
import json
import logging
from typing import Dict, Any, Optional

class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434", timeout: int = 30):
        """
        Initialize Ollama client
        
        Args:
            base_url: Ollama server URL
            timeout: Request timeout in seconds
        """
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def generate_response(self, prompt: str, model: str = "llama3.1:8b", 
                         stream: bool = False, **kwargs) -> Dict[str, Any]:
        """
        Generate response from Ollama model
        
        Args:
            prompt: User input prompt
            model: Model name to use
            stream: Whether to stream response
            **kwargs: Additional parameters
            
        Returns:
            Dictionary containing response or error
        """
        try:
            url = f"{self.base_url}/api/generate"
            
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": stream,
                **kwargs
            }
            
            self.logger.info(f"Sending request to {url} with model: {model}")
            
            response = self.session.post(
                url, 
                json=payload, 
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            
            if "response" in data:
                self.logger.info("Successfully received response")
                return {
                    "success": True,
                    "response": data["response"],
                    "model": model,
                    "prompt": prompt
                }
            else:
                self.logger.error(f"No response field in data: {data}")
                return {
                    "success": False,
                    "error": "No response field in server response",
                    "raw_data": data
                }
                
        except requests.exceptions.ConnectionError:
            error_msg = "Cannot connect to Ollama server. Make sure Ollama is running."
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}
            
        except requests.exceptions.Timeout:
            error_msg = f"Request timeout after {self.timeout} seconds"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}
            
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP error: {e}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}
            
        except json.JSONDecodeError:
            error_msg = "Invalid JSON response from server"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}
            
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    def list_models(self) -> Dict[str, Any]:
        """
        Get list of available models
        
        Returns:
            Dictionary containing models list or error
        """
        try:
            url = f"{self.base_url}/api/tags"
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            return {"success": True, "models": data.get("models", [])}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def check_connection(self) -> bool:
        """
        Check if Ollama server is accessible
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            url = f"{self.base_url}/api/tags"
            response = self.session.get(url, timeout=5)
            return response.status_code == 200
        except:
            return False