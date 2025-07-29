from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import os
import uuid
from ollama_client import OllamaClient
from config import Config
from utils.helpers import validate_input, clean_response

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize Ollama client
ollama_client = OllamaClient(
    base_url=Config.OLLAMA_BASE_URL,
    timeout=Config.OLLAMA_TIMEOUT
)

@app.route('/')
def index():
    """Main chat page"""
    # Initialize session
    if 'chat_id' not in session:
        session['chat_id'] = str(uuid.uuid4())
    if 'messages' not in session:
        session['messages'] = []
    
    return render_template('index.html', 
                         title=Config.APP_TITLE,
                         models=Config.AVAILABLE_MODELS,
                         default_model=Config.DEFAULT_MODEL)

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        model = data.get('model', Config.DEFAULT_MODEL)
        temperature = float(data.get('temperature', Config.DEFAULT_TEMPERATURE))
        
        # Validate input
        validation = validate_input(user_message, Config.MAX_MESSAGE_LENGTH)
        if not validation['valid']:
            return jsonify({
                'success': False,
                'error': '; '.join(validation['errors'])
            }), 400
        
        # Add user message to session
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_msg = {
            'role': 'user',
            'content': user_message,
            'timestamp': timestamp
        }
        
        if 'messages' not in session:
            session['messages'] = []
        session['messages'].append(user_msg)
        
        # Generate AI response
        response = ollama_client.generate_response(
            prompt=user_message,
            model=model,
            temperature=temperature
        )
        
        if response['success']:
            # Clean and add bot response
            clean_content = clean_response(response['response'])
            bot_msg = {
                'role': 'assistant',
                'content': clean_content,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'model': model
            }
            session['messages'].append(bot_msg)
            
            # Limit chat history
            if len(session['messages']) > Config.MAX_CHAT_HISTORY:
                session['messages'] = session['messages'][-Config.MAX_CHAT_HISTORY:]
            
            session.modified = True
            
            return jsonify({
                'success': True,
                'response': clean_content,
                'model': model,
                'timestamp': bot_msg['timestamp']
            })
        else:
            return jsonify({
                'success': False,
                'error': response['error']
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/models', methods=['GET'])
def get_models():
    """Get available models"""
    try:
        models_response = ollama_client.list_models()
        if models_response['success']:
            return jsonify({
                'success': True,
                'models': [model['name'] for model in models_response['models']]
            })
        else:
            return jsonify({
                'success': True,
                'models': Config.AVAILABLE_MODELS
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get Ollama connection status"""
    try:
        is_connected = ollama_client.check_connection()
        return jsonify({
            'success': True,
            'connected': is_connected,
            'url': Config.OLLAMA_BASE_URL
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/clear', methods=['POST'])
def clear_chat():
    """Clear chat history"""
    try:
        session['messages'] = []
        session.modified = True
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get chat history"""
    try:
        messages = session.get('messages', [])
        return jsonify({
            'success': True,
            'messages': messages,
            'total': len(messages)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('logs', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    # Run Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )