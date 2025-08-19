from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/api/health', methods=['GET'])
def health():
    """Simple health check"""
    return jsonify({
        'status': 'healthy',
        'openai_key_present': bool(os.getenv('OPENAI_API_KEY')),
        'port': os.getenv('PORT', 'not set'),
        'railway_env': os.getenv('RAILWAY_ENVIRONMENT', 'not set')
    })

@app.route('/api/test', methods=['GET'])  
def test():
    """Simple test endpoint"""
    return jsonify({'message': 'Backend is working!'})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8085))
    app.run(debug=False, host='0.0.0.0', port=port)
